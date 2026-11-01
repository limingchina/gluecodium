import com.here.gluecodium.Gluecodium;
import com.here.gluecodium.cli.OptionReader;
import com.here.gluecodium.loader.LimeBasedLimeModelLoader;
import java.nio.file.Path;

/** Repeated full API pipeline; output paths are unique, caching is disabled. */
public final class WarmJvm {
    public static void main(String[] args) throws Exception {
        if (args.length != 3) throw new IllegalArgumentException("INPUT OUTPUT_BASE ITERATIONS");
        var parsed = OptionReader.INSTANCE.read(new String[]{"-input", args[0], "-generators", "cpp", "-output", args[1]});
        if (parsed == null) throw new IllegalArgumentException("options rejected");
        var cli = parsed.getFirst(); var generator = parsed.getSecond();
        for (int i = 0; i < Integer.parseInt(args[2]); i++) {
            String output = Path.of(args[1], Integer.toString(i)).toString();
            cli.setOutputDir(output); cli.setCommonOutputDir(output);
            long start = System.nanoTime();
            boolean ok = new Gluecodium(cli, generator, new LimeBasedLimeModelLoader()).execute();
            long elapsed = System.nanoTime() - start;
            System.out.println(i + " " + elapsed + " " + ok);
            if (!ok) System.exit(1);
        }
    }
}
