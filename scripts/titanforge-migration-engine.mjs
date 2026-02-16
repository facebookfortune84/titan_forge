// scripts/titanforge-migration-engine.mjs
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import * as babelParser from "@babel/parser";
import traversePkg from "@babel/traverse"; const traverse = traversePkg.default;
import generate from "@babel/generator";
import { diffLines } from "diff";
import diff2htmlPkg from "diff2html";

const { Diff2Html } = diff2htmlPkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT = path.resolve(__dirname, "..", "frontend", "src");
const exts = [".tsx", ".ts", ".jsx", ".js"];

const files = [];
const report = {
  root: ROOT,
  processedFiles: 0,
  modifiedFiles: 0,
  entries: [],
};

function walk(dir) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full);
    else if (exts.includes(path.extname(e.name))) files.push(full);
  }
}

function parse(code, filePath) {
  return babelParser.parse(code, {
    sourceType: "module",
    plugins: ["typescript", "jsx"],
    sourceFilename: filePath,
  });
}

function rewriteAliasToRelative(importPath, filePath) {
  if (!importPath.startsWith("@/")) return importPath;
  const subPath = importPath.slice(2);
  const fromDir = path.dirname(filePath);
  const target = path.join(ROOT, subPath);
  let rel = path.relative(fromDir, target).replace(/\\/g, "/");
  if (!rel.startsWith(".")) rel = "./" + rel;
  return rel;
}

function transformAST(ast, filePath, originalCode) {
  const changes = [];
  let usesLazy = false;
  let hasSuspenseImport = false;

  traverse(ast, {
    ImportDeclaration(pathImp) {
      const source = pathImp.node.source.value;

      // Next.js imports → remove or replace
      if (source === "next/dynamic") {
        changes.push("Replaced next/dynamic with React.lazy");
        pathImp.node.source.value = "react";
        pathImp.node.specifiers = [
          babelParser.parse("import { lazy, Suspense } from 'react';").program
            .body[0].specifiers[0],
          babelParser.parse("import { lazy, Suspense } from 'react';").program
            .body[0].specifiers[1],
        ];
      }

      if (source === "next/link") {
        changes.push("Replaced next/link with react-router-dom Link");
        pathImp.node.source.value = "react-router-dom";
        pathImp.node.specifiers = [
          babelParser.parse("import { Link } from 'react-router-dom';").program
            .body[0].specifiers[0],
        ];
      }

      if (source === "next/image") {
        changes.push("Removed next/image import");
        pathImp.remove();
        return;
      }

      if (source === "next/navigation") {
        changes.push("Replaced next/navigation with react-router-dom useNavigate");
        pathImp.node.source.value = "react-router-dom";
        pathImp.node.specifiers = [
          babelParser.parse(
            "import { useNavigate } from 'react-router-dom';"
          ).program.body[0].specifiers[0],
        ];
      }

      if (source === "next/head") {
        changes.push("Removed next/head import");
        pathImp.remove();
        return;
      }

      // Track Suspense import
      if (source === "react") {
        for (const spec of pathImp.node.specifiers) {
          if (
            spec.type === "ImportSpecifier" &&
            spec.imported.name === "Suspense"
          ) {
            hasSuspenseImport = true;
          }
        }
      }

      // Alias rewrite @/...
      const newSource = rewriteAliasToRelative(source, filePath);
      if (newSource !== source) {
        changes.push(`Alias import "${source}" → "${newSource}"`);
        pathImp.node.source.value = newSource;
      }
    },

    CallExpression(pathCall) {
      const callee = pathCall.node.callee;
      if (callee.type === "Identifier" && callee.name === "lazy") {
        usesLazy = true;
      }
    },

    JSXElement(pathJSX) {
      const opening = pathJSX.node.openingElement;
      const name = opening.name;

      // <Image ...> → <img ...>
      if (name.type === "JSXIdentifier" && name.name === "Image") {
        changes.push("Converted <Image> to <img>");
        name.name = "img";
      }

      // <Link href="..."> → <Link to="...">
      if (name.type === "JSXIdentifier" && name.name === "Link") {
        for (const attr of opening.attributes) {
          if (
            attr.type === "JSXAttribute" &&
            attr.name.name === "href"
          ) {
            changes.push('Converted <Link href="..."> to <Link to="...">');
            attr.name.name = "to";
          }
        }
      }
    },
  });

  // If lazy() used but no Suspense import, add Suspense to react import
  if (usesLazy && !hasSuspenseImport) {
    traverse(ast, {
      ImportDeclaration(pathImp) {
        if (pathImp.node.source.value === "react") {
          const hasSuspenseAlready = pathImp.node.specifiers.some(
            (s) =>
              s.type === "ImportSpecifier" && s.imported.name === "Suspense"
          );
          if (!hasSuspenseAlready) {
            changes.push("Added Suspense to react import for lazy()");
            pathImp.node.specifiers.push(
              babelParser.parse(
                "import { Suspense } from 'react';"
              ).program.body[0].specifiers[0]
            );
          }
        }
      },
    });
  }

  const output = generate(ast, { retainLines: true }, originalCode).code;
  const modified = output !== originalCode;

  return { modified, output, changes };
}

function generateHtmlDiff(fileRel, before, after) {
  const diff = diffLines(before, after);
  const unified = diff
    .map((part) => {
      const prefix = part.added ? "+" : part.removed ? "-" : " ";
      return part.value
        .split("\n")
        .map((line) => (line ? prefix + line : ""))
        .join("\n");
    })
    .join("\n");

  const html = Diff2Html.getPrettyHtml(unified, {
    inputFormat: "diff",
    showFiles: false,
    matching: "lines",
  });

  return `<h2>${fileRel}</h2>${html}`;
}

walk(ROOT);

console.log(`Scanning ${files.length} files under ${ROOT}...\n`);

let htmlSections = [];

for (const file of files) {
  const rel = path.relative(ROOT, file);
  const original = fs.readFileSync(file, "utf8");

  let ast;
  try {
    ast = parse(original, file);
  } catch (e) {
    console.warn(`Skipping (parse error): ${rel}`);
    continue;
  }

  const { modified, output, changes } = transformAST(ast, file, original);

  report.processedFiles++;

  if (modified) {
    fs.writeFileSync(file, output, "utf8");
    report.modifiedFiles++;
    report.entries.push({ file: rel, changes });
    const section = generateHtmlDiff(rel, original, output);
    htmlSections.push(section);
    console.log(`Updated: ${rel}`);
  }
}

const reportPathJson = path.resolve(__dirname, "..", "migration-report.json");
fs.writeFileSync(reportPathJson, JSON.stringify(report, null, 2), "utf8");

const reportPathHtml = path.resolve(__dirname, "..", "migration-report.html");
const htmlDoc = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>TitanForge Migration Report</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/diff2html/bundles/css/diff2html.min.css" />
<style>
body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; padding: 20px; background: #05060a; color: #e5e7eb; }
h1, h2 { color: #facc15; }
a { color: #38bdf8; }
</style>
</head>
<body>
<h1>TitanForge Migration Report</h1>
<p>Root: ${ROOT}</p>
<p>Processed files: ${report.processedFiles}</p>
<p>Modified files: ${report.modifiedFiles}</p>
${htmlSections.join("\n")}
</body>
</html>`;

fs.writeFileSync(reportPathHtml, htmlDoc, "utf8");

console.log("\nDone.");
console.log(`Processed: ${report.processedFiles} files`);
console.log(`Modified:  ${report.modifiedFiles} files`);
console.log(`JSON report:  ${reportPathJson}`);
console.log(`HTML report:  ${reportPathHtml}`);
console.log("Now run: npm run build");