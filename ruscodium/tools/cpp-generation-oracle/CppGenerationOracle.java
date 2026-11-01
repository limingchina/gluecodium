import com.here.gluecodium.GluecodiumOptions;
import com.here.gluecodium.cli.OptionReader;
import com.here.gluecodium.generator.common.GeneratedFile;
import com.here.gluecodium.generator.common.GeneratorOptions;
import com.here.gluecodium.generator.common.templates.TemplateEngine;
import com.here.gluecodium.generator.cpp.CppGenerator;
import com.here.gluecodium.loader.LimeBasedLimeModelLoader;
import com.here.gluecodium.model.lime.*;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/** Records the real generator's complete outputs and bounded frontend views. */
public final class CppGenerationOracle {
    private static Map<String,Object> map(Object... entries) {
        Map<String,Object> result = new LinkedHashMap<>();
        for (int i = 0; i < entries.length; i += 2) result.put((String)entries[i], entries[i + 1]);
        return result;
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: CppGenerationOracle GROUP OUTPUT");
        String group = args[0]; Path output = Path.of(args[1]);
        boolean rawComments = "1".equals(System.getenv("CPP_ORACLE_RAW_COMMENTS"));
        Files.createDirectories(output);
        String base = "ruscodium/tools/cpp-generation-oracle/";
        boolean legacy = Set.of("default", "custom").contains(group);
        boolean docs = group.equals("docs");
        String scenario = group.startsWith("comments-file-") ? "comments" : group;
        String smoke = "gluecodium/src/test/resources/smoke/" + scenario + "/";
        List<String> main = legacy || docs ? List.of(base + group + ".lime") : List.of(smoke + "input");
        List<String> aux = legacy || docs ? (group.equals("custom") ? List.of(base + "aux.lime") : List.of()) :
            (Files.isDirectory(Path.of(smoke + "auxiliary")) ? List.of(smoke + "auxiliary") : List.of());
        GeneratorOptions options = new GeneratorOptions();
        Map<String,String> placeholders = Collections.emptyMap();
        if (docs) placeholders = Map.of("subject", "configured {@Cpp replacement}{@Java alternative}");
        if (!legacy && !docs) {
            Path argsFile = Path.of(smoke + "input/commandlineoptions.txt");
            if (Files.exists(argsFile)) {
                String raw = Files.readString(argsFile).replace("$INPUT_FOLDER", smoke + "input").replace("$AUX_FOLDER", smoke + "auxiliary");
                var parsed = OptionReader.INSTANCE.read(raw.trim().split("\\s+"));
                if (parsed == null) throw new IllegalArgumentException("smoke options rejected");
                GluecodiumOptions cli = parsed.getFirst(); options = parsed.getSecond(); placeholders = cli.getDocsPlaceholders();
            } else {
                options.setCppInternalNamespace(List.of("gluecodium")); options.setInternalPrefix("foobar_");
            }
            if (group.equals("comments-file-interface")) main = List.of(smoke + "input/CommentsInterface.lime");
            if (group.equals("comments-file-lambda")) main = List.of(smoke + "input/CommentsLambda.lime");
        }
        Files.writeString(output.resolve("stage.txt"), "load\n");
        LimeModel model = new LimeBasedLimeModelLoader().loadModel(main, aux, placeholders);
        Map<String,Object> jobOptions = map();
        if (group.equals("custom")) {
            options.setCppRootNamespace(List.of("acme", "api"));
            options.setCppInternalNamespace(List.of("acme", "detail"));
            options.setCppExport("ACME_API"); options.setCppExportCommon("ACME_COMMON");
            options.setCopyrightHeaderContents("Copyright 2026 Example\nAll rights reserved.");
            jobOptions = map("root_namespace", options.getCppRootNamespace(), "internal_namespace", options.getCppInternalNamespace(),
                "export", options.getCppExport(), "export_common", options.getCppExportCommon(),
                "copyright_header", options.getCopyrightHeaderContents());
        }
        if (!legacy) {
            jobOptions = map("root_namespace", options.getCppRootNamespace(), "internal_namespace", options.getCppInternalNamespace(),
                "export", options.getCppExport(), "export_common", options.getCppExportCommon(), "copyright_header", options.getCopyrightHeaderContents());
            if (jobOptions.get("export_common") == null) jobOptions.remove("export_common");
            if (!options.getTags().isEmpty()) jobOptions.put("tags", new TreeSet<>(options.getTags()).stream().toList());
            Map<String,Object> metadata = map("main", main, "aux", aux, "placeholders", new TreeMap<>(placeholders),
                "root_namespace", options.getCppRootNamespace(), "internal_namespace", options.getCppInternalNamespace(),
                "export", options.getCppExport(), "export_common", options.getCppExportCommon(), "copyright_header", options.getCopyrightHeaderContents(),
                "tags", new TreeSet<>(options.getTags()).stream().toList(), "internal_prefix", options.getInternalPrefix(),
                "werror", new TreeSet<>(options.getWerror()).stream().toList(), "profile", "unfiltered-loader-model");
            Files.writeString(output.resolve("metadata.json"), ReferenceModel.jsonString(metadata));
        }
        Files.writeString(output.resolve("stage.txt"), "generator\n");
        TemplateEngine.INSTANCE.initCopyrightHeaderContents(options.getCopyrightHeaderContents());
        CppGenerator generator = new CppGenerator(); generator.initialize(options);
        List<GeneratedFile> generated = generator.generate(model);
        Files.writeString(output.resolve("stage.txt"), "export\n");
        ReferenceModel graph = new ReferenceModel();
        graph.incrementalSnapshotDocument(model);
        Map<String,Object> overlays = new LinkedHashMap<>();
        int observed = 0;
        while (observed < graph.discoveredObjects().size()) {
          for (int i = observed; i < graph.discoveredObjects().size(); i++) {
            observed = i + 1;
            Object obj = graph.discoveredObjects().get(i); Map<String,Object> props = new LinkedHashMap<>();
            if (obj instanceof LimeNamedElement) {
                props.put("name", ((LimeNamedElement)obj).getName());
                props.put("fullName", ((LimeNamedElement)obj).getFullName());
            }
            if (obj instanceof LimeComment && !rawComments) props.put("isEmpty", ((LimeComment)obj).isEmpty());
            if (obj instanceof LimeType) props.put("actualType", graph.value(((LimeType)obj).getActualType(), "actualType"));
            if (obj instanceof LimeReturnType) props.put("isVoid", ((LimeReturnType)obj).isVoid());
            if (obj instanceof LimeFunction) props.put("exception", graph.value(((LimeFunction)obj).getException(), "exception"));
            if (obj instanceof LimeEnumeration) props.put("uniqueEnumerators", graph.value(((LimeEnumeration)obj).getUniqueEnumerators(), "uniqueEnumerators"));
            if (obj instanceof LimeStruct) props.put("uninitializedFields", graph.value(((LimeStruct)obj).getUninitializedFields(), "uninitializedFields"));
            if (obj instanceof LimeFieldConstructor) {
                props.put("fields", graph.value(((LimeFieldConstructor)obj).getFields(), "fields"));
                props.put("struct", graph.value(((LimeFieldConstructor)obj).getStruct(), "struct"));
            }
            if (!props.isEmpty()) overlays.put("n" + (i + 1), props);
          }
          // Getter results can introduce objects whose own fields reveal more objects.
          graph.incrementalSnapshotDocument(model);
        }
        Map<String,Object> snapshot = graph.incrementalSnapshotDocument(model);
        Map<String,Object> absent = new LinkedHashMap<>();
        List<String> candidates = List.of("propertyElement", "isVirtual", "isConst", "isAsyncHelper", "internalNamespace",
            "exportName", "functionUsings", "needsExport", "storageQualifier", "structElement", "struct", "iter", "constructorComment");
        for (int i = 0; i < graph.discoveredObjects().size(); i++) {
            Object obj = graph.discoveredObjects().get(i);
            if (!(obj instanceof LimeElement)) continue;
            List<String> missing = new ArrayList<>();
            for (String property : candidates) {
                String suffix = Character.toUpperCase(property.charAt(0)) + property.substring(1);
                boolean present = Arrays.stream(obj.getClass().getMethods()).anyMatch(method -> method.getParameterCount() == 0 &&
                    (method.getName().equals("get" + suffix) || method.getName().equals(property) || method.getName().equals("is" + suffix)));
                if (!present) missing.add(property);
            }
            if (!missing.isEmpty()) absent.put("n" + (i + 1), missing);
        }
        Map<String,Object> job = map("schema", "gluecodium.cpp-generation-job", "version", 1, "snapshot", snapshot,
            "property_overlays", overlays, "absent_properties", absent, "options", jobOptions);
        if (rawComments) {
            // Versioned opt-in capture of source facts, not getFor() or formatted text.
            Field sections = LimeComment.class.getDeclaredField("taggedSections");
            if (!Modifier.isPrivate(sections.getModifiers()) || !List.class.equals(sections.getType()))
                throw new IllegalStateException("LimeComment taggedSections field shape changed");
            sections.setAccessible(true);
            Map<String,Object> comments = new LinkedHashMap<>();
            for (int i = 0; i < graph.discoveredObjects().size(); i++) {
                Object obj = graph.discoveredObjects().get(i);
                if (!(obj instanceof LimeComment)) continue;
                Object value = sections.get(obj);
                if (!(value instanceof List<?>)) throw new IllegalStateException("invalid taggedSections list");
                List<Object> pairs = new ArrayList<>();
                for (Object item : (List<?>)value) {
                    if (!(item instanceof kotlin.Pair<?,?>)) throw new IllegalStateException("invalid taggedSections pair");
                    kotlin.Pair<?,?> pair = (kotlin.Pair<?,?>)item;
                    if (!(pair.getFirst() instanceof String) || !(pair.getSecond() instanceof String))
                        throw new IllegalStateException("invalid taggedSections strings");
                    pairs.add(List.of(pair.getFirst(), pair.getSecond()));
                }
                comments.put("n" + (i + 1), pairs);
            }
            job.put("version", 2); job.put("raw_comments", comments);
        }
        TreeMap<String,String> inventory = new TreeMap<>();
        for (GeneratedFile file : generated) {
            String path = file.getTargetFile().toPath().toString().replace('\\', '/');
            if (inventory.put(path, file.getSourceSet().name()) != null) throw new IllegalStateException("Duplicate output " + path);
        }
        Files.createDirectories(output);
        Files.writeString(output.resolve("job.json"), ReferenceModel.jsonString(job), StandardCharsets.UTF_8);
        Files.writeString(output.resolve("manifest.json"), ReferenceModel.jsonString(map("files", inventory)), StandardCharsets.UTF_8);
        for (GeneratedFile file : generated) {
            Path target = output.resolve("files").resolve(file.getTargetFile().toPath());
            Files.createDirectories(target.getParent());
            Files.writeString(target, file.getContent(), StandardCharsets.UTF_8);
        }
        if (!legacy) Files.writeString(output.resolve("stage.txt"), "complete\n");
        else Files.deleteIfExists(output.resolve("stage.txt"));
        System.out.println(group + ": " + generated.size() + " generated files, " + graph.discoveredObjects().size() + " model nodes");
    }
}
