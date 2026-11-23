// news-image-20261122 — entrypoint (Node 22, standard library only).
//
// The entry image ships in this repository as entry.png (drawn at build
// time by draw_entry.py). This program's only job is to place a copy of
// it where the make.fun grader looks: $MAKEFUN_OUTPUT_DIR/entry.png,
// defaulting to /output. It creates the output directory if needed.
// No network, no randomness, no clock — the same input bytes always
// produce the same output bytes, so both graded runs are identical.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outputDir, "entry.png"));
