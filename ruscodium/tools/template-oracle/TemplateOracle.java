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
        var scalarEach = engine.compileMustache("negative-each-scalar", "{{#each name}}{{this}}{{/each}}");
        try {
            scalarEach.render(map("name", "outer"));
            throw new IllegalStateException("each on a scalar unexpectedly rendered");
        } catch (MustacheException error) {
            checkError(error, "RENDER_HELPER_INVALID_OPTIONS");
        }
    }
    private static void compileError(MustacheEngine engine, String name, String template, String code) {
        try {
            engine.compileMustache("negative-" + name, template);
            throw new IllegalStateException(name + " unexpectedly compiled");
        } catch (MustacheException error) {
            checkError(error, code);
        }
    }
    private static void checkError(MustacheException error, String code) {
        if (error.getClass() != MustacheException.class || !error.getMessage().startsWith(code + ":")) throw error;
    }
    private static void fixture(Path dir, String name, String template, Object data) throws Exception {
        var hooks = map("names", List.of(), "predicates", List.of(), "sorters", List.of());
        var request = map("schema", "gluecodium.template.render-request", "version", 1,
            "template", template, "data", data, "property_overlays", map(), "hooks", hooks);
        String output = TemplateEngine.INSTANCE.render(template, data, Map.of(), Map.of(), Map.of());
        save(dir.resolve(name + ".request.json"), ReferenceModel.jsonString(request));
        save(dir.resolve(name + ".expected"), output);
    }
    private static void modelFixture(Path dir, LimeModel model, Object element, String caseName, String template) throws Exception {
        ReferenceModel graph = new ReferenceModel();
        Object data = graph.value(element, "data");
        var opts = new GeneratorOptions();
        var rules = new CppNameRules(List.of(), NameRuleSetLoaderKt.nameRuleSetFromConfig(opts.getCppNameRules()));
        var cache = new CppNameCache(List.of(), model.getReferenceMap(), rules);
        var original = new CppNameResolver(model.getReferenceMap(), List.of("internal"), cache,
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
        Map<String,Object> snapshot = graph.snapshotDocument(element);
        Map<String,Object> overlays = new LinkedHashMap<>();
        for (int i = 0; i < graph.discoveredObjects().size(); i++) {
            Object obj = graph.discoveredObjects().get(i); Map<String,Object> props = new LinkedHashMap<>();
            if (obj instanceof LimeComment) props.put("isEmpty", ((LimeComment)obj).isEmpty());
            if (obj instanceof LimeType) props.put("actualType", graph.value(((LimeType)obj).getActualType(), "actualType"));
            if (obj instanceof LimeReturnType) props.put("isVoid", ((LimeReturnType)obj).isVoid());
            if (obj instanceof LimeFunction) props.put("exception", graph.value(((LimeFunction)obj).getException(), "exception"));
            if (obj instanceof LimeEnumeration) props.put("uniqueEnumerators", graph.value(((LimeEnumeration)obj).getUniqueEnumerators(), "uniqueEnumerators"));
            if (!props.isEmpty()) overlays.put("n" + (i + 1), props);
        }
        // Overlay getter results can discover additional model nodes; complete the graph after observations.
        snapshot = graph.snapshotDocument(element);
        // Record only named properties whose Java bean accessors are actually absent.
        // These are known context lookups used by the selected production partials.
        Map<String,Object> absent = new LinkedHashMap<>();
        for (int i = 0; i < graph.discoveredObjects().size(); i++) {
            Object obj = graph.discoveredObjects().get(i);
            if (!(obj instanceof LimeElement)) continue;
            List<String> missing = new ArrayList<>();
            for (String property : List.of("propertyElement", "isVirtual", "isConst", "isAsyncHelper", "internalNamespace")) {
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
        fixture(out, "helpers", "oracle/helpers", map("yes", true, "no", false,
            "items", List.of("one", "two", "three"), "multiline", "alpha  \n beta\t\n",
            "special", "<a & \"b\">\n", "empty", List.of(), "nil", null));
        fixture(out, "partials", "oracle/partials", map("value", "VALUE"));
        fixture(out, "export-default", "cpp/common/Export", map("internalNamespace", List.of("example", "internal"), "exportName", "GLUE"));
        fixture(out, "export-empty", "cpp/common/Export", map("internalNamespace", List.of(), "exportName", ""));
        for (var entry : pending.entrySet()) Files.write(entry.getKey(), entry.getValue());
    }
}
