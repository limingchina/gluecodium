import com.here.gluecodium.generator.common.GeneratedFile;
import com.here.gluecodium.generator.common.GeneratorOptions;
import com.here.gluecodium.generator.common.templates.TemplateEngine;
import com.here.gluecodium.generator.cpp.CppGenerator;
import com.here.gluecodium.loader.LimeBasedLimeModelLoader;
import com.here.gluecodium.model.lime.*;
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
        if (args.length != 2 || !Set.of("default", "custom").contains(args[0]))
            throw new IllegalArgumentException("usage: CppGenerationOracle default|custom OUTPUT");
        String group = args[0]; Path output = Path.of(args[1]);
        String base = "ruscodium/tools/cpp-generation-oracle/";
        List<String> main = List.of(base + group + ".lime");
        List<String> aux = group.equals("custom") ? List.of(base + "aux.lime") : List.of();
        LimeModel model = new LimeBasedLimeModelLoader().loadModel(main, aux, Collections.emptyMap());
        GeneratorOptions options = new GeneratorOptions();
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
        TemplateEngine.INSTANCE.initCopyrightHeaderContents(options.getCopyrightHeaderContents());
        CppGenerator generator = new CppGenerator(); generator.initialize(options);
        List<GeneratedFile> generated = generator.generate(model);
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
            if (obj instanceof LimeComment) props.put("isEmpty", ((LimeComment)obj).isEmpty());
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
        System.out.println(group + ": " + generated.size() + " generated files, " + graph.discoveredObjects().size() + " model nodes");
    }
}
