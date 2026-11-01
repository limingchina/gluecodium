import com.here.gluecodium.loader.LimeBasedLimeModelLoader;
import com.here.gluecodium.model.lime.LimeAttributes;
import com.here.gluecodium.model.lime.LimeAttributeType;
import com.here.gluecodium.model.lime.LimeAttributeValueType;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/** Experimental snapshot of backed public model properties, not a Rust AST. */
public final class ReferenceModel {
    private static final String PREFIX = "com.here.gluecodium.model.lime.";
    private final IdentityHashMap<Object, String> ids = new IdentityHashMap<>();
    private final List<Object> queue = new ArrayList<>();
    private final List<Object> stableNodes = new ArrayList<>();
    private final Path repository = Path.of("").toAbsolutePath().normalize();

    /** Objects discovered so far, in snapshot ID order; intended for bounded oracle observations. */
    public List<Object> discoveredObjects() { return Collections.unmodifiableList(queue); }

    public Object value(Object x, String path) throws Exception {
        if (x instanceof Double && !Double.isFinite((Double)x) || x instanceof Float && !Float.isFinite((Float)x))
            throw new IllegalArgumentException(path + ": non-finite number");
        if (x == null || x instanceof Boolean || x instanceof Number) return x;
        if (x instanceof Character) return x.toString();
        if (x instanceof String) return x;
        if (x instanceof Enum<?>) { Map<String,Object> e = new LinkedHashMap<>(); e.put("enum", x.getClass().getName()); e.put("name", ((Enum<?>)x).name()); return e; }
        if (x instanceof List<?> && !x.getClass().getName().startsWith(PREFIX)) {
            List<Object> out = new ArrayList<>(); int i = 0;
            for (Object item : (List<?>)x) out.add(value(item, path + "[" + i++ + "]"));
            return out;
        }
        if (x instanceof Map<?, ?> && !x.getClass().getName().startsWith(PREFIX)) {
            TreeMap<String, Object> sorted = new TreeMap<>();
            for (Map.Entry<?, ?> e : ((Map<?, ?>)x).entrySet()) {
                if (!(e.getKey() instanceof String)) throw new IllegalArgumentException(path + ": unsupported map key " + e.getKey().getClass().getName());
                sorted.put((String)e.getKey(), e.getValue());
            }
            Map<String,Object> out = new LinkedHashMap<>();
            for (var e : sorted.entrySet()) out.put(e.getKey(), value(e.getValue(), path + "[" + e.getKey() + "]"));
            return out;
        }
        if (!x.getClass().getName().startsWith(PREFIX)) throw new IllegalArgumentException(path + ": unsupported value " + x.getClass().getName());
        String id = ids.get(x);
        if (id == null) { id = "n" + (queue.size() + 1); ids.put(x, id); queue.add(x); }
        return Map.of("$ref", id);
    }

    private Map<String,Object> node(Object x, String id) throws Exception {
        TreeMap<String,Method> properties = new TreeMap<>();
        for (Class<?> c = x.getClass(); c != null && c.getName().startsWith(PREFIX); c = c.getSuperclass()) {
            for (Field f : c.getDeclaredFields()) {
                if (Modifier.isStatic(f.getModifiers()) || f.isSynthetic() || f.getName().contains("$")) continue;
                String name = f.getName();
                String getter = name.startsWith("is") && name.length() > 2 && Character.isUpperCase(name.charAt(2)) ? name : "get" + Character.toUpperCase(name.charAt(0)) + name.substring(1);
                try {
                    Method m = x.getClass().getMethod(getter);
                    if (m.getParameterCount() == 0 && !Modifier.isStatic(m.getModifiers())) properties.putIfAbsent(name, m);
                } catch (NoSuchMethodException ignored) { /* private implementation field */ }
            }
        }
        if (x instanceof com.here.gluecodium.model.lime.LimeElementRef<?>)
            properties.put("element", x.getClass().getMethod("getElement"));
        if (x instanceof com.here.gluecodium.model.lime.LimeTypeRef)
            properties.put("type", x.getClass().getMethod("getType"));
        Map<String,Object> props = new LinkedHashMap<>();
        if (x instanceof LimeAttributes) {
            LimeAttributes attributes = (LimeAttributes)x;
            Map<String,Object> exported = new TreeMap<>();
            for (LimeAttributeType type : LimeAttributeType.values()) {
                if (!attributes.have(type)) continue;
                Map<String,Object> values = new TreeMap<>();
                for (LimeAttributeValueType kind : attributes.getAllAttributeValueTypes(type))
                    values.put(kind.name(), value(attributes.get(type, kind, Object.class), id + ".attributes." + type.name() + "." + kind.name()));
                exported.put(type.name(), values);
            }
            props.put("attributes", exported);
        }
        for (var e : properties.entrySet()) {
            String path = id + "." + e.getKey();
            try {
                Object v = e.getValue().invoke(x);
                if (x instanceof com.here.gluecodium.model.lime.LimeModel && e.getKey().equals("fileNameMap")) {
                    Map<String,String> normalized = new TreeMap<>();
                    for (var entry : ((com.here.gluecodium.model.lime.LimeModel)x).getFileNameMap().entrySet()) {
                        Path file = Path.of(entry.getValue()).toAbsolutePath().normalize();
                        normalized.put(entry.getKey(), file.startsWith(repository) ? repository.relativize(file).toString().replace('\\', '/') : entry.getValue());
                    }
                    v = normalized;
                }
                props.put(e.getKey(), value(v, path));
            }
            catch (InvocationTargetException ex) { throw new IllegalArgumentException(path + ": getter failed", ex.getCause()); }
        }
        Map<String,Object> result = new LinkedHashMap<>();
        result.put("id", id); result.put("class", x.getClass().getName()); result.put("properties", props);
        return result;
    }
    public Map<String,Object> snapshotDocument(Object model) throws Exception {
        Object root = value(model, "root");
        List<Object> nodes = new ArrayList<>();
        for (int i = 0; i < queue.size(); i++) nodes.add(node(queue.get(i), "n" + (i + 1)));
        Map<String,Object> doc = new LinkedHashMap<>();
        doc.put("schema", "gluecodium.reference-model.snapshot"); doc.put("version", 1); doc.put("root", root); doc.put("nodes", nodes);
        return doc;
    }
    /** Incremental snapshot for observations that can discover more objects. Each node's
     * getters are read once, preserving identity when a getter constructs a fresh view. */
    public Map<String,Object> incrementalSnapshotDocument(Object model) throws Exception {
        Object root = value(model, "root");
        for (int i = stableNodes.size(); i < queue.size(); i++)
            stableNodes.add(node(queue.get(i), "n" + (i + 1)));
        Map<String,Object> doc = new LinkedHashMap<>();
        doc.put("schema", "gluecodium.reference-model.snapshot"); doc.put("version", 1);
        doc.put("root", root); doc.put("nodes", new ArrayList<>(stableNodes));
        return doc;
    }
    private String snapshot(Object model) throws Exception {
        return jsonString(snapshotDocument(model));
    }
    public static String jsonString(Object x) {
        StringBuilder b = new StringBuilder(); json(b, x); return b.append('\n').toString();
    }
    public static void json(StringBuilder b, Object x) {
        if (x == null) b.append("null");
        else if (x instanceof String) {
            b.append('"'); for (char c : ((String)x).toCharArray()) { switch(c) {
                case '"': b.append("\\\""); break; case '\\': b.append("\\\\"); break; case '\n': b.append("\\n"); break; case '\r': b.append("\\r"); break; case '\t': b.append("\\t"); break;
                default: if (c < 32) b.append(String.format("\\u%04x", (int)c)); else b.append(c);
            }} b.append('"');
        } else if (x instanceof Boolean || x instanceof Number) b.append(x);
        else if (x instanceof List<?>) { b.append('['); boolean first = true; for (Object v : (List<?>)x) { if (!first) b.append(','); first = false; json(b,v); } b.append(']'); }
        else if (x instanceof Map<?,?>) { b.append('{'); boolean first = true; for (var e : ((Map<?,?>)x).entrySet()) { if (!first) b.append(','); first = false; json(b,e.getKey()); b.append(':'); json(b,e.getValue()); } b.append('}'); }
        else throw new IllegalArgumentException("Unsupported JSON value");
    }
    private static List<String> discover(List<String> sources) throws Exception {
        SortedSet<String> files = new TreeSet<>();
        for (String source : sources) {
            Path path = Path.of(source.startsWith("~/") ? System.getProperty("user.home") + source.substring(1) : source).toAbsolutePath().normalize();
            if (!Files.exists(path)) throw new IllegalArgumentException("Source does not exist: " + source);
            if (Files.isDirectory(path)) {
                try (var paths = Files.walk(path)) {
                    paths.filter(p -> !Files.isDirectory(p) && p.getFileName().toString().endsWith(".lime"))
                         .map(p -> p.toAbsolutePath().normalize().toString()).forEach(files::add);
                }
            } else if (Files.isRegularFile(path) && path.getFileName().toString().endsWith(".lime")) files.add(path.toString());
            else throw new IllegalArgumentException("Source must be a directory or .lime file: " + source);
        }
        return new ArrayList<>(files);
    }
    public static void main(String[] args) throws Exception {
        List<String> main = new ArrayList<>(), aux = new ArrayList<>(); Path output = null;
        for (int i=0; i<args.length; i++) {
            if (i+1 >= args.length) throw new IllegalArgumentException("Expected value after " + args[i]);
            switch(args[i]) { case "--main": main.add(args[++i]); break; case "--aux": aux.add(args[++i]); break; case "--output": output = Path.of(args[++i]); break; default: throw new IllegalArgumentException("Unknown option " + args[i]); }
        }
        if (main.isEmpty() && aux.isEmpty()) throw new IllegalArgumentException("Supply --main or --aux");
        main = discover(main); aux = discover(aux);
        if (main.isEmpty() && aux.isEmpty()) throw new IllegalArgumentException("No .lime source files found");
        String document = new ReferenceModel().snapshot(new LimeBasedLimeModelLoader().loadModel(main, aux, Collections.emptyMap()));
        if (output == null) System.out.print(document); else Files.writeString(output, document, StandardCharsets.UTF_8);
    }
}
