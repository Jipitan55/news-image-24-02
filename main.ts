import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry: copy the pre-rendered infographic to the output directory.
// The program runs offline, twice, and must write identical bytes both times.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

copyFileSync(source, target);

// Verify the copy is complete: the output must be byte-identical to the
// source, otherwise fail loudly instead of shipping a truncated image.
const expected = readFileSync(source);
const written = readFileSync(target);
if (!written.equals(expected)) {
  throw new Error(`entry.png copy mismatch: wrote ${written.length} bytes, expected ${expected.length}`);
}
console.log(`wrote ${target} (${written.length} bytes)`);
