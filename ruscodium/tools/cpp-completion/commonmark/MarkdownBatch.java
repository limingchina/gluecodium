import com.vladsch.flexmark.parser.Parser;
import com.vladsch.flexmark.formatter.Formatter;
import java.nio.file.*;
public final class MarkdownBatch {
 public static void main(String[] args)throws Exception {
  var parser=Parser.builder().build(); var formatter=Formatter.builder().build();
  var out=Path.of(args[1]); Files.createDirectories(out);
  try(var files=Files.list(Path.of(args[0]))) {
   for(var path:files.filter(x->x.toString().endsWith(".md")).sorted().toList()) {
    var input=Files.readString(path);
    var output=formatter.render(parser.parse(kotlin.text.StringsKt.trim(input).toString()));
    Files.writeString(out.resolve(path.getFileName()),kotlin.text.StringsKt.trim(output).toString());
   }
  }
 }
}
