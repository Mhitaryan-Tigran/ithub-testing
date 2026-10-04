import { readFileSync, readdirSync } from "node:fs";
import { PGlite } from "@electric-sql/pglite";

const here = new URL("./", import.meta.url);

export async function freshDb() {
  const db = new PGlite();
  await db.exec(readFileSync(new URL("schema.sql", here), "utf8"));
  await db.exec(readFileSync(new URL("seed.sql", here), "utf8"));
  return db;
}

export function queries() {
  return Object.fromEntries(readdirSync(new URL("queries/", here)).sort().map((file) => [file.replace(/^\d+_|\.sql$/g, ""), readFileSync(new URL(`queries/${file}`, here), "utf8")]));
}
