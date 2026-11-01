import com.here.gluecodium.generator.common.templates.TemplateEngine;
import java.nio.charset.StandardCharsets;
import com.here.gluecodium.loader.LimeBasedLimeModelLoader;
import com.here.gluecodium.model.lime.*;
import com.here.gluecodium.generator.common.*;
import com.here.gluecodium.generator.cpp.*;
import com.here.gluecodium.common.LimeLogger;
import kotlin.jvm.functions.Function1;
import java.util.logging.Logger;
import java.nio.file.*;
import java.util.*;
import org.trimou.engine.MustacheEngine;
import org.trimou.exception.MustacheException;

public final class TemplateOracle {
    private static final Map<Path, byte[]> pending = new LinkedHashMap<>();
    private static void save(Path path, String contents) { pending.put(path, contents.getBytes(StandardCharsets.UTF_8)); }
    private static Map<String,Object> map(Object... pairs) {
        Map<String,Object> out = new LinkedHashMap<>();
        for (int i = 0; i < pairs.length; i += 2) out.put((String)pairs[i], pairs[i+1]);
        return out;
    }
    // Use the same engine instance as TemplateEngine.render, and check the phase
    // and Trimou error code rather than accepting an arbitrary failure.
    private static void negativeCases() throws Exception {
        var field = TemplateEngine.class.getDeclaredField("engine");
        field.setAccessible(true);
        MustacheEngine engine = (MustacheEngine) field.get(null);
        compileError(engine, "if-no-args", "{{#if}}YES{{/if}}", "COMPILE_HELPER_VALIDATION_FAILURE");
        compileError(engine, "unless-no-args", "{{#unless}}YES{{/unless}}", "COMPILE_HELPER_VALIDATION_FAILURE");
        compileError(engine, "set-positional", "{{#set name}}{{name}}{{/set}}", "COMPILE_HELPER_VALIDATION_FAILURE");
        compileError(engine, "inline-redefinition", "{{+p}}A{{/p}}{{>p}}{{+p}}B{{/p}}{{>p}}", "COMPILE_NESTED_TEMPLATE_ERROR");
        compileError(engine, "inactive-prefix", "{{#no}}{{prefix}}{{/no}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Insufficient number of parameters - expected: 1");
        compileError(engine, "capitalize-arity", "{{capitalize}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Insufficient number of parameters - expected: 1");
        compileError(engine, "join-arity", "{{join delimiter=\",\"}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Insufficient number of parameters - expected: 1");
        compileError(engine, "join-partial-arity", "{{joinPartial}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Insufficient number of parameters - expected: 1");
        compileError(engine, "set-join-arity", "{{#setJoin \"x\" \"a\" delimiter=\",\"}}{{x}}{{/setJoin}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Insufficient number of parameters - expected: 3");
        compileError(engine, "set-join-delimiter", "{{#setJoin \"x\" \"a\" \"b\" other=\",\"}}{{x}}{{/setJoin}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Required hash key delimiter not found");
        compileError(engine, "inactive-if-value", "{{#no}}{{if one}}{{/no}}", "COMPILE_HELPER_VALIDATION_FAILURE", "Unsupported tag type");
        for (String helper : List.of("capitalize", "escape")) {
            var nullArgument = engine.compileMustache("negative-null-" + helper, "{{" + helper + " nil}}");
            try {
                nullArgument.render(map("nil", null));
                throw new IllegalStateException(helper + " with null unexpectedly rendered");
            } catch (NullPointerException error) {
                if (error.getClass() != NullPointerException.class) throw error;
            }
        }
        var nullPartial = engine.compileMustache("negative-null-join-partial", "{{+p}}X{{/p}}{{joinPartial nil \"p\" \",\"}}");
        try {
            nullPartial.render(map("nil", null));
            throw new IllegalStateException("joinPartial with null unexpectedly rendered");
        } catch (NullPointerException error) {
            if (error.getClass() != NullPointerException.class) throw error;
        }
        var scalarEach = engine.compileMustache("negative-each-scalar", "{{#each name}}{{this}}{{/each}}");
        try {
            scalarEach.render(map("name", "outer"));
            throw new IllegalStateException("each on a scalar unexpectedly rendered");
        } catch (MustacheException error) {
            checkError(error, "RENDER_HELPER_INVALID_OPTIONS");
        }
    }
    private static void compileError(MustacheEngine engine, String name, String template, String code) {
        compileError(engine, name, template, code, "");
    }
    private static void compileError(MustacheEngine engine, String name, String template, String code, String detail) {
        try {
            engine.compileMustache("negative-" + name, template);
            throw new IllegalStateException(name + " unexpectedly compiled");
        } catch (MustacheException error) {
            checkError(error, code);
            if (!error.getMessage().contains(detail)) throw error;
        }
    }
    private static void checkError(MustacheException error, String code) {
        if (error.getClass() != MustacheException.class || !error.getMessage().startsWith(code + ":")) throw error;
    }
    private static void negativeSortCases(LimeModel model) {
        var refs = model.getReferenceMap();
        LimeType a = (LimeType)Objects.requireNonNull(refs.get("m9.matrix.Service"));
        LimeType b = (LimeType)Objects.requireNonNull(refs.get("m9.matrix.PlainService"));
        var attrs = new LimeAttributes.Builder().build();
        var first = new LimeTypeAlias(a.getPath(), new LimeComment(), attrs, new LimeDirectTypeRef(b, false, attrs));
        var second = new LimeTypeAlias(b.getPath(), new LimeComment(), attrs, new LimeDirectTypeRef(a, false, attrs));
        checkSortFailure(List.of(first, second));
        checkSortFailure(List.of(a, a));
    }
    private static void checkSortFailure(List<LimeNamedElement> elements) {
        try {
            new TopologicalSort(elements).sort();
            throw new IllegalStateException("Sorter unexpectedly accepted cycle or duplicate identity");
        } catch (com.here.gluecodium.cli.GluecodiumExecutionException error) {
            if (error.getClass() != com.here.gluecodium.cli.GluecodiumExecutionException.class ||
                !"Cycle detected in C++ elements dependencies.".equals(error.getMessage())) throw error;
        }
    }
    private static void excludedComment(Object receiver, Class<?> owner, String name, LimeComment original) throws Exception {
        var field = owner.getDeclaredField(name);
        field.setAccessible(true);
        field.set(receiver, original.withExcluded(true));
    }
    private static void setPlatformSkips(LimeFunction receiver, Boolean javaValue) throws Exception {
        var builder = new LimeAttributes.Builder();
        builder.addAttribute(LimeAttributeType.JAVA, LimeAttributeValueType.SKIP, javaValue);
        builder.addAttribute(LimeAttributeType.KOTLIN, LimeAttributeValueType.SKIP, true);
        builder.addAttribute(LimeAttributeType.SWIFT, LimeAttributeValueType.SKIP, true);
        var field = LimeElement.class.getDeclaredField("attributes");
        field.setAccessible(true);
        field.set(receiver, builder.build());
    }
    private static void fixture(Path dir, String name, String template, Object data) throws Exception {
        var hooks = map("names", List.of(), "predicates", List.of(), "sorters", List.of());
        var request = map("schema", "gluecodium.template.render-request", "version", 1,
            "template", template, "data", data, "property_overlays", map(), "hooks", hooks);
        String output = TemplateEngine.INSTANCE.render(template, data, Map.of(), Map.of(), Map.of());
        save(dir.resolve(name + ".request.json"), ReferenceModel.jsonString(request));
        save(dir.resolve(name + ".expected"), output);
    }
    private static void emptyFilterFixture(Path dir, LimeModel model) throws Exception {
        var registered = new CppGeneratorPredicates(model.getReferenceMap()).getPredicates();
        var calls = new ArrayList<Object>();
        Map<String,Function1<Object,Boolean>> checks = new LinkedHashMap<>();
        for (var entry : registered.entrySet()) {
            String name = entry.getKey(); Function1<Object,Boolean> delegate = entry.getValue();
            checks.put(name, receiver -> { calls.add(receiver); return delegate.invoke(receiver); });
        }
        var data = map("items", List.of());
        String template = "oracle/empty-filter";
        String output = TemplateEngine.INSTANCE.render(template, data, Map.of(), checks, Map.of());
        if (!calls.isEmpty()) throw new IllegalStateException("Empty filter unexpectedly evaluated a predicate");
        var registry = new ArrayList<>(registered.keySet());
        Collections.sort(registry);
        var hooks = map("names", List.of(), "predicates", List.of(), "sorters", List.of(),
            "registered_predicates", registry);
        var request = map("schema", "gluecodium.template.render-request", "version", 1,
            "template", template, "data", data, "property_overlays", map(), "hooks", hooks);
        save(dir.resolve("empty-filter.request.json"), ReferenceModel.jsonString(request));
        save(dir.resolve("empty-filter.expected"), output);
    }
    private static void modelFixture(Path dir, LimeModel model, Object element, String caseName, String template) throws Exception {
        modelFixture(dir, model, element, element, caseName, template);
    }
    private static void modelFixture(Path dir, LimeModel model, Object element, Object snapshotRoot, String caseName, String template) throws Exception {
        modelFixture(dir, model, element, snapshotRoot, caseName, template, List.of(), List.of("internal"));
    }
    private static void modelFixture(Path dir, LimeModel model, Object element, Object snapshotRoot, String caseName, String template, List<String> rootNamespace, List<String> internalNamespace) throws Exception {
        ReferenceModel graph = new ReferenceModel();
        Object data = graph.value(element, "data");
        var opts = new GeneratorOptions();
        var rules = new CppNameRules(rootNamespace, NameRuleSetLoaderKt.nameRuleSetFromConfig(opts.getCppNameRules()));
        var cache = new CppNameCache(rootNamespace, model.getReferenceMap(), rules);
        var original = new CppNameResolver(model.getReferenceMap(), internalNamespace, cache,
            new LimeLogger(Logger.getLogger("template-oracle"), model.getFileNameMap()), new DoxygenCommentsProcessor(false), false, false);
        var full = new CppFullNameResolver(cache);
        var names = new ArrayList<Object>();
        var predicates = new ArrayList<Object>();
        Map<String,NameResolver> resolvers = new LinkedHashMap<>();
        for (String key : List.of("", "C++", "FQN")) {
            NameResolver delegate = key.equals("FQN") ? full : original;
            resolvers.put(key, new NameResolver() {
                private String capture(String mode, Object receiver, String result) {
                    try { names.add(map("resolver", key, "mode", mode, "receiver", graph.value(receiver, "name.receiver"), "result", result)); }
                    catch (Exception e) { throw new RuntimeException(e); }
                    return result;
                }
                public String resolveName(Object x) { return capture("name", x, delegate.resolveName(x)); }
                public String resolveGetterName(Object x) { return capture("getter", x, delegate.resolveGetterName(x)); }
                public String resolveSetterName(Object x) { return capture("setter", x, delegate.resolveSetterName(x)); }
                public String resolveReferenceName(Object x) { return capture("ref", x, delegate.resolveReferenceName(x)); }
            });
        }
        Map<String,Function1<Object,Boolean>> checks = new LinkedHashMap<>();
        for (var entry : new CppGeneratorPredicates(model.getReferenceMap()).getPredicates().entrySet()) {
            String key = entry.getKey(); Function1<Object,Boolean> delegate = entry.getValue();
            checks.put(key, x -> { boolean result = delegate.invoke(x); try {
                predicates.add(map("name", key, "receiver", graph.value(x, "predicate.receiver"), "result", result));
            } catch (Exception e) { throw new RuntimeException(e); } return result; });
        }
        List<Object> sortRecords = new ArrayList<>();
        Map<String, Function1<List<? extends Object>, List<? extends Object>>> sorters = new LinkedHashMap<>();
        sorters.put("", input -> {
            List<LimeNamedElement> selected = new ArrayList<>();
            for (Object value : input) if (value instanceof LimeNamedElement) selected.add((LimeNamedElement)value);
            List<LimeNamedElement> result = new TopologicalSort(selected).sort();
            try { sortRecords.add(map("name", "", "input", graph.value(input, "sort.input"),
                "result", graph.value(result, "sort.result"))); }
            catch (Exception e) { throw new RuntimeException(e); }
            return result;
        });
        String output = TemplateEngine.INSTANCE.render(template, element, resolvers, checks, sorters);
        Map<String,Object> snapshot = graph.snapshotDocument(snapshotRoot);
        Map<String,Object> overlays = new LinkedHashMap<>();
        for (int i = 0; i < graph.discoveredObjects().size(); i++) {
            Object obj = graph.discoveredObjects().get(i); Map<String,Object> props = new LinkedHashMap<>();
            if (caseName.startsWith("m9-") && obj instanceof LimeNamedElement) {
                props.put("name", ((LimeNamedElement)obj).getName());
                props.put("fullName", ((LimeNamedElement)obj).getFullName());
            }
            if (obj instanceof LimeComment) props.put("isEmpty", ((LimeComment)obj).isEmpty());
            if (obj instanceof LimeType) props.put("actualType", graph.value(((LimeType)obj).getActualType(), "actualType"));
            if (obj instanceof LimeReturnType) props.put("isVoid", ((LimeReturnType)obj).isVoid());
            if (obj instanceof LimeFunction) props.put("exception", graph.value(((LimeFunction)obj).getException(), "exception"));
            if (obj instanceof LimeEnumeration) props.put("uniqueEnumerators", graph.value(((LimeEnumeration)obj).getUniqueEnumerators(), "uniqueEnumerators"));
            if (!props.isEmpty()) overlays.put("n" + (i + 1), props);
        }
        // Overlay getter results can discover additional model nodes; complete the graph after observations.
        snapshot = graph.snapshotDocument(snapshotRoot);
        // Record only named properties whose Java bean accessors are actually absent.
        // These are known context lookups used by the selected production partials.
        Map<String,Object> absent = new LinkedHashMap<>();
        for (int i = 0; i < graph.discoveredObjects().size(); i++) {
            Object obj = graph.discoveredObjects().get(i);
            if (!(obj instanceof LimeElement)) continue;
            List<String> missing = new ArrayList<>();
            var candidates = new ArrayList<>(List.of("propertyElement", "isVirtual", "isConst", "isAsyncHelper", "internalNamespace"));
            if (caseName.equals("review-sort")) candidates.add("iter");
            if (caseName.startsWith("m9-")) candidates.addAll(List.of("exportName", "functionUsings", "needsExport", "storageQualifier"));
            for (String property : candidates) {
                String suffix = Character.toUpperCase(property.charAt(0)) + property.substring(1);
                boolean present = Arrays.stream(obj.getClass().getMethods()).anyMatch(method ->
                    method.getParameterCount() == 0 && (method.getName().equals("get" + suffix) ||
                    method.getName().equals(property) || method.getName().equals("is" + suffix)));
                if (!present) missing.add(property);
            }
            if (!missing.isEmpty()) absent.put("n" + (i + 1), missing);
        }
        var request = map("schema", "gluecodium.template.render-request", "version", 1,
            "template", template, "data", data, "snapshot", snapshot, "property_overlays", overlays, "absent_properties", absent,
            "hooks", map("names", names, "predicates", predicates, "sorters", sortRecords));
        save(dir.resolve(caseName + ".request.json"), ReferenceModel.jsonString(request));
        save(dir.resolve(caseName + ".expected"), output);
    }
    public static void main(String[] args) throws Exception {
        Path out = Path.of(args[0]); Files.createDirectories(out);
        negativeCases();
        LimeModel model = new LimeBasedLimeModelLoader().loadModel(
            List.of(Path.of("ruscodium/tools/template-oracle/fixture.lime").toAbsolutePath().toString()), List.of(), Map.of());
        LimeModel nativeModel = new LimeBasedLimeModelLoader().loadModel(
            List.of(Path.of("ruscodium/tools/template-oracle/native.lime").toAbsolutePath().toString()), List.of(), Map.of());
        LimeModel m9Model = new LimeBasedLimeModelLoader().loadModel(
            List.of(Path.of("ruscodium/tools/template-oracle/m9.lime").toAbsolutePath().toString()), List.of(), Map.of());
        negativeSortCases(m9Model);
        var m9refs = m9Model.getReferenceMap();
        List<Object> m9elements = new ArrayList<>(), m9types = new ArrayList<>();
        for (var entry : new TreeMap<>(m9refs).entrySet()) {
            if (!entry.getKey().startsWith("m9.matrix.")) continue;
            Object value = entry.getValue();
            m9elements.add(value);
            if (value instanceof LimeField) m9types.add(((LimeField)value).getTypeRef());
        }
        Object alias = Objects.requireNonNull(m9refs.get("m9.matrix.Outer.EAlias"));
        Object enumeration = Objects.requireNonNull(m9refs.get("m9.matrix.Outer.E"));
        Object service = Objects.requireNonNull(m9refs.get("m9.matrix.Service"));
        Object kind = Objects.requireNonNull(m9refs.get("m9.matrix.Kind"));
        Object kinds = Objects.requireNonNull(m9refs.get("m9.matrix.Kinds"));
        Object callback = Objects.requireNonNull(m9refs.get("m9.matrix.Callback"));
        Object withFunction = Objects.requireNonNull(m9refs.get("m9.matrix.WithFunction"));
        Object choice = Objects.requireNonNull(m9refs.get("m9.matrix.Outer.CHOICE"));
        Object method = Objects.requireNonNull(m9refs.get("m9.matrix.WithFunction.take"));
        List<Object> extraOrders = List.of(
            List.of(kinds, callback, withFunction, kind),
            List.of(choice, enumeration, "filtered scalar", m9types.get(0)),
            List.of(kind, callback, kinds, withFunction), List.of(method, kind));
        modelFixture(out, m9Model, map("refs", m9types, "elements", m9elements,
            "order", List.of(alias, service, enumeration), "reverse", List.of(enumeration, service, alias),
            "sorted", List.of(service, enumeration, alias), "extraOrders", extraOrders), m9Model,
            "m9-matrix", "oracle/m9-matrix", List.of(), List.of());
        modelFixture(out, m9Model, Objects.requireNonNull(m9refs.get("m9.matrix.Outer")), m9Model,
            "m9-class", "cpp/CppClass", List.of(), List.of());
        modelFixture(out, m9Model, Objects.requireNonNull(m9refs.get("m9.matrix.Container")), m9Model,
            "m9-struct", "cpp/CppStruct", List.of(), List.of());
        // Use a separately loaded real model so that the targeted excluded-comment
        // mutations do not alter any other fixture. Each value still comes from
        // the JVM model and each predicate result is measured by the real registry.
        LimeModel commentsModel = new LimeBasedLimeModelLoader().loadModel(
            List.of(Path.of("ruscodium/tools/template-oracle/m9.lime").toAbsolutePath().toString()), List.of(), Map.of());
        var commentRefs = commentsModel.getReferenceMap();
        LimeFunction returnCase = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.returnCase");
        LimeFunction parameterCase = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.parameterCase");
        LimeFunction thrownCase = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.thrownCase");
        LimeFunction ownCase = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.ownCase");
        LimeStruct constructorStruct = (LimeStruct)commentRefs.get("m9.matrix.ExplicitPartial");
        excludedComment(returnCase.getReturnType(), LimeReturnType.class, "comment", returnCase.getReturnType().getComment());
        excludedComment(parameterCase.getParameters().get(0), LimeNamedElement.class, "comment", parameterCase.getParameters().get(0).getComment());
        excludedComment(thrownCase.getThrownType(), LimeThrownType.class, "comment", thrownCase.getThrownType().getComment());
        excludedComment(ownCase, LimeNamedElement.class, "comment", ownCase.getComment());
        excludedComment(constructorStruct, LimeStruct.class, "constructorComment", constructorStruct.getConstructorComment());
        LimeFunction falseSkip = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.falseSkip");
        LimeFunction nullSkip = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.nullSkip");
        LimeFunction trueSkip = (LimeFunction)commentRefs.get("m9.matrix.CommentCases.trueSkip");
        setPlatformSkips(falseSkip, false);
        setPlatformSkips(nullSkip, null);
        setPlatformSkips(trueSkip, true);
        modelFixture(out, commentsModel, map("elements", List.of(returnCase, parameterCase, thrownCase, ownCase,
            constructorStruct.getFieldConstructors().get(0)), "skips", List.of(falseSkip, nullSkip, trueSkip)), commentsModel,
            "m9-comments", "oracle/m9-comments", List.of(), List.of());
        var refs = nativeModel.getReferenceMap();
        for (var entry : Map.of("native-enumeration", "native.matrix.Shade", "native-alias", "native.matrix.Labels",
                "native-function", "native.matrix.Service.fetchURL", "native-return", "native.matrix.Service.fetchURL").entrySet()) {
            String template = entry.getKey().equals("native-enumeration") ? "cpp/CppEnumeration" :
                entry.getKey().equals("native-alias") ? "cpp/CppTypeAlias" :
                entry.getKey().equals("native-function") ? "cpp/CppFunctionSignature" : "cpp/CppReturnType";
            Object root = Objects.requireNonNull(refs.get(entry.getValue()), entry.getValue());
            modelFixture(out, nativeModel, root, nativeModel, entry.getKey(), template, List.of(), List.of());
        }
        List<Object> named = new ArrayList<>(), types = new ArrayList<>(), accessors = new ArrayList<>();
        for (String key : List.of("native.matrix.Shade", "native.matrix.Shade.RED", "native.matrix.Shade.BLUE",
                "native.matrix.Labels", "native.matrix.Flag", "native.matrix.ServiceAlias", "native.matrix.InterfaceAlias",
                "native.matrix.Service", "native.matrix.Service.NestedThing", "native.matrix.Service.NestedThing.someURLValue",
                "native.matrix.Service.fetchURL", "native.matrix.Service.SOME_COUNT", "native.matrix.Data", "native.matrix.Data.HTTPServer", "native.matrix.Data.httpURL2", "native.matrix.Data.leading__underscores", "native.matrix.Worker")) {
            named.add(map("label", key, "value", Objects.requireNonNull(refs.get(key), key)));
        }
        for (var entry : new TreeMap<>(refs).entrySet()) {
            if (entry.getKey().startsWith("native.matrix.Data.") && entry.getValue() instanceof LimeField) {
                LimeField field = (LimeField)entry.getValue();
                types.add(map("label", entry.getKey(), "value", field.getTypeRef()));
                accessors.add(map("label", entry.getKey(), "value", field));
            }
        }
        for (String key : List.of("native.matrix.Service.isReady", "native.matrix.Service.customValue"))
            accessors.add(map("label", key, "value", Objects.requireNonNull(refs.get(key), key)));
        accessors.add(map("label", "native.matrix.Plain.flag", "value", refs.get("native.matrix.Plain.flag")));
        for (String key : List.of("SOME_COUNT", "FRACTION", "TEXT", "ENABLED", "FAVORITE")) {
            LimeConstant constant = (LimeConstant)Objects.requireNonNull(refs.get("native.matrix.Service." + key));
            types.add(map("label", "constant-value-" + key, "value", constant.getValue()));
        }
        for (LimeBasicType.TypeId typeId : LimeBasicType.TypeId.values())
            types.add(map("label", "basic-type-id-" + typeId.name(), "value", typeId));
        LimeFunction run = (LimeFunction)Objects.requireNonNull(refs.get("native.matrix.Worker.run"));
        types.add(map("label", "void-return", "value", run.getReturnType()));
        modelFixture(out, nativeModel, map("named", named, "types", types, "accessors", accessors), nativeModel,
            "native-matrix", "oracle/native-names", List.of("outer", "api"), List.of("detail", "impl"));
        emptyFilterFixture(out, model);
        modelFixture(out, model, model.getReferenceMap().get("oracle.Color"), "cpp-enumeration", "cpp/CppEnumeration");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Labels"), "cpp-alias", "cpp/CppTypeAlias");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Service.convert"), "cpp-function", "cpp/CppFunctionSignature");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Service.convert"), "cpp-return", "cpp/CppReturnType");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Service.risky"), "cpp-function-throws", "cpp/CppFunctionSignature");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Service.risky"), "cpp-return-throws", "cpp/CppReturnType");
        fixture(out, "inline-eof", "oracle/inline-eof", map("value", "VALUE"));
        fixture(out, "inline-middle", "oracle/inline-middle", map("value", "VALUE"));
        modelFixture(out, model, model.getReferenceMap().get("oracle.Service.register"), "cpp-function-static", "cpp/CppFunctionSignature");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Info.status"), "name-arguments", "oracle/name-arguments");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Color"), "model-helpers", "oracle/model-helpers");
        modelFixture(out, model, model.getReferenceMap().get("oracle.Color"), "review-sort", "oracle/review-sort");
        var attributes = new LimeAttributes.Builder()
            .addAttribute(LimeAttributeType.CPP, LimeAttributeValueType.FULL_NAME, "Foo")
            .addAttribute(LimeAttributeType.SWIFT, LimeAttributeValueType.OPTION_SET, true)
            .build();
        modelFixture(out, model, map("attrs", attributes), attributes, "review-attributes", "oracle/review-attributes");
        try {
            TemplateEngine.INSTANCE.render("oracle/nested-comment", map("value", "ignored"), Map.of(), Map.of(), Map.of());
            throw new IllegalStateException("Nested comment unexpectedly compiled");
        } catch (org.trimou.exception.MustacheException expected) {
            if (!expected.getMessage().contains("COMPILE_INVALID_TAG")) throw expected;
        }
        fixture(out, "prefix-cr", "oracle/prefix-cr", map("value", "one  \r\ntwo\rthree  \n"));
        fixture(out, "adjacent-comment", "oracle/adjacent-comment", map("x", false, "y", false));
        fixture(out, "adjacent-sections", "oracle/adjacent-sections", map("x", false, "y", false));
        fixture(out, "join-partial", "oracle/join-partial", map("outer", "O",
            "entries", List.of(map("name", "A"), map("name", "B")), "single", map("name", "C")));
        fixture(out, "eval", "oracle/eval", map("key", "chosen", "absent", "missing",
            "lookup", map("chosen", map("name", "selected"))));
        fixture(out, "truth", "oracle/truth", map("zero", 0, "one", 1, "no", false,
            "emptyString", "", "emptyMap", map(), "nil", null));
        fixture(out, "scope", "oracle/scope", map("name", "outer", "items", new ArrayList<>(List.of("a", "b"))));
        fixture(out, "review-helpers", "oracle/review-helpers", map("nil", null, "one", 1,
            "special", "x\rY\bZ\f"));
        fixture(out, "review-scope", "oracle/review-scope", map("items", new ArrayList<>(List.of("a", "b"))));
        fixture(out, "review-selectors", "oracle/review-selectors", map("values", map("a]b", "bracket")));
        fixture(out, "review-values", "oracle/review-values", map("items", List.of("a", "b"), "nil", null));
        fixture(out, "helpers", "oracle/helpers", map("yes", true, "no", false,
            "items", List.of("one", "two", "three"), "multiline", "alpha  \n beta\t\n",
            "special", "<a & \"b\">\n", "empty", List.of(), "nil", null));
        fixture(out, "partials", "oracle/partials", map("value", "VALUE"));
        fixture(out, "export-default", "cpp/common/Export", map("internalNamespace", List.of("example", "internal"), "exportName", "GLUE"));
        fixture(out, "export-empty", "cpp/common/Export", map("internalNamespace", List.of(), "exportName", ""));
        for (var entry : pending.entrySet()) Files.write(entry.getKey(), entry.getValue());
    }
}
