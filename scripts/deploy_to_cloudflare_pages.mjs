#!/usr/bin/env node
/**
 * Build CardScanR dist/ for Cloudflare Pages from docs/ + beta worktree assets.
 * Usage: node scripts/deploy_to_cloudflare_pages.mjs [--deploy]
 */
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DOCS = join(ROOT, "docs");
const DIST = join(ROOT, "dist");
const BETA_WORKTREE = join(
  "D:",
  "CardScanR_worktrees",
  "public_beta_signup_foundation_20260805",
  "public_website"
);

const LEGAL_JS = new Set(["site.js", "site.css"]);
const deploy = process.argv.includes("--deploy");

function copyLegalSite() {
  if (existsSync(DIST)) {
    rmSync(DIST, { recursive: true, force: true });
  }
  mkdirSync(DIST, { recursive: true });
  cpSync(DOCS, DIST, { recursive: true });
}

function copyBetaAssets() {
  const betaSrc = join(BETA_WORKTREE, "beta");
  const betaDist = join(DIST, "beta");
  if (existsSync(betaSrc)) {
    cpSync(betaSrc, betaDist, { recursive: true });
    console.log("Copied beta/ from worktree");
  } else {
    console.warn("Beta worktree not found — dist will omit /beta/ until worktree is available");
  }

  for (const rel of [
    "assets/css/beta.css",
    "assets/js/beta.js",
    "assets/js/config.js",
  ]) {
    const src = join(BETA_WORKTREE, rel);
    const dest = join(DIST, rel);
    if (!existsSync(src)) {
      console.warn(`Missing beta asset: ${src}`);
      continue;
    }
    const filename = rel.split("/").pop();
    if (LEGAL_JS.has(filename)) {
      console.warn(`Skipping ${rel} — would overwrite legal site asset`);
      continue;
    }
    mkdirSync(dirname(dest), { recursive: true });
    cpSync(src, dest);
    console.log(`Copied ${rel}`);
  }
}

function mergeRedirects() {
  const legal = join(DOCS, "_redirects");
  const beta = join(BETA_WORKTREE, "_redirects");
  const parts = [];
  if (existsSync(legal)) parts.push(readFileSync(legal, "utf8").trim());
  if (existsSync(beta)) {
    const betaLines = readFileSync(beta, "utf8")
      .trim()
      .split("\n")
      .filter((line) => line && !line.startsWith("/support"));
    parts.push(betaLines.join("\n"));
  }
  writeFileSync(join(DIST, "_redirects"), parts.filter(Boolean).join("\n") + "\n", "utf8");
}

function mergeHeaders() {
  const legal = join(DOCS, "_headers");
  const beta = join(BETA_WORKTREE, "_headers");
  const parts = [];
  if (existsSync(legal)) parts.push(readFileSync(legal, "utf8").trim());
  if (existsSync(beta)) parts.push(readFileSync(beta, "utf8").trim());
  writeFileSync(join(DIST, "_headers"), parts.filter(Boolean).join("\n\n") + "\n", "utf8");
}

function main() {
  console.log("Building dist/ from docs/ …");
  copyLegalSite();
  copyBetaAssets();
  mergeRedirects();
  mergeHeaders();

  writeFileSync(
    join(DIST, "BUILD_INFO.txt"),
    [
      "cardscanr-legal-site",
      `built_at=${new Date().toISOString()}`,
      `deploy_flag=${deploy}`,
    ].join("\n"),
    "utf8"
  );

  console.log(`Built ${DIST}`);

  if (deploy) {
    console.log("Deploying to Cloudflare Pages (cardscanr-www) …");
    execSync(
      "npx --yes wrangler@4 pages deploy dist --project-name=cardscanr-www --branch=main --commit-dirty=true",
      {
        cwd: ROOT,
        stdio: "inherit",
        shell: true,
      }
    );
    console.log("Deploy complete");
  } else {
    console.log("Dry build only. Pass --deploy to publish.");
  }
}

main();
