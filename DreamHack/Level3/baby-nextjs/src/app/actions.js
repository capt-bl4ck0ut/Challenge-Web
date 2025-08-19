'use server';

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function getFlag() {
  return { message: readFileSync(resolve(__dirname, '../../flag.txt'), 'utf8') };
}
