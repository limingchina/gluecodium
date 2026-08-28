// Minimal static file server with COOP/COEP headers so that the pthread build
// can use SharedArrayBuffer in a browser. Run from this directory:
//
//   node serve.mjs [port]
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL(".", import.meta.url));
const port = Number(process.argv[2]) || 8080;

const contentTypes = {
    ".html": "text/html",
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".wasm": "application/wasm",
};

createServer(async (request, response) => {
    const path = request.url === "/" ? "/test.html" : request.url.split("?")[0];
    try {
        const body = await readFile(join(root, path));
        response.writeHead(200, {
            "Content-Type": contentTypes[extname(path)] ?? "application/octet-stream",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Embedder-Policy": "require-corp",
        });
        response.end(body);
    } catch {
        response.writeHead(404).end();
    }
}).listen(port, () => console.log(`serving ${root} at http://localhost:${port}`));
