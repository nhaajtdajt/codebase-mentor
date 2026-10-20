#!/usr/bin/env python3
"""Quét nhanh một repo để lấy điểm xuất phát cho codebase-explainer.

Chỉ đọc, không ghi gì. Chỉ dùng thư viện chuẩn.

Cách dùng:
    python scan_repo.py <gốc-repo> [--max-tree-depth 3]

In ra (Markdown): manifest & stack đoán được, số file theo ngôn ngữ, cây thư mục
rút gọn, file cấu hình, ứng viên entry point, TODO/FIXME/HACK, tóm tắt git.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist", "build",
    "target", "out", ".next", ".nuxt", ".svelte-kit", ".turbo", ".cache", "coverage",
    ".idea", ".gradle", "vendor", "bin", "obj", ".pytest_cache", ".mypy_cache",
    ".parcel-cache", ".output", "storybook-static", ".terraform",
}

LANG_BY_EXT = {
    ".ts": "TypeScript", ".tsx": "TypeScript (TSX)", ".js": "JavaScript", ".jsx": "JavaScript (JSX)",
    ".mjs": "JavaScript", ".cjs": "JavaScript", ".vue": "Vue", ".svelte": "Svelte",
    ".py": "Python", ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin script", ".go": "Go",
    ".rs": "Rust", ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".cpp": "C++", ".cc": "C++",
    ".c": "C", ".h": "C/C++ header", ".swift": "Swift", ".dart": "Dart", ".scala": "Scala",
    ".sol": "Solidity", ".sql": "SQL", ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
    ".sh": "Shell", ".ps1": "PowerShell", ".graphql": "GraphQL", ".gql": "GraphQL",
    ".proto": "Protobuf", ".prisma": "Prisma", ".ipynb": "Jupyter",
}

MANIFESTS = {
    "package.json": "Node/JS/TS", "pom.xml": "Java (Maven)", "build.gradle": "JVM (Gradle)",
    "build.gradle.kts": "JVM (Gradle Kotlin)", "settings.gradle": "JVM (Gradle)",
    "pyproject.toml": "Python", "requirements.txt": "Python", "setup.py": "Python",
    "Pipfile": "Python", "go.mod": "Go", "Cargo.toml": "Rust", "composer.json": "PHP",
    "Gemfile": "Ruby", "pubspec.yaml": "Dart/Flutter", "foundry.toml": "Solidity (Foundry)",
    "deno.json": "Deno", "turbo.json": "Monorepo (Turborepo)", "nx.json": "Monorepo (Nx)",
    "pnpm-workspace.yaml": "Monorepo (pnpm)", "lerna.json": "Monorepo (Lerna)",
}

CONFIG_PATTERNS = [
    r"^tsconfig.*\.json$", r"^jsconfig\.json$", r"^vite\.config\.", r"^webpack\.config\.",
    r"^next\.config\.", r"^nuxt\.config\.", r"^svelte\.config\.", r"^astro\.config\.",
    r"^angular\.json$", r"^babel\.config\.", r"^\.babelrc", r"^tailwind\.config\.",
    r"^postcss\.config\.", r"^\.eslintrc", r"^eslint\.config\.", r"^\.prettierrc",
    r"^prettier\.config\.", r"^biome\.json", r"^\.editorconfig$", r"^\.nvmrc$",
    r"^\.node-version$", r"^\.env\.example$", r"^\.env\.sample$", r"^\.env\.template$",
    r"^\.env(\..+)?$", r"^Dockerfile", r"^docker-compose.*\.ya?ml$", r"^compose.*\.ya?ml$",
    r"^\.dockerignore$", r"^nginx.*\.conf$", r"^application.*\.(ya?ml|properties)$",
    r"^bootstrap.*\.ya?ml$", r"^jest\.config\.", r"^vitest\.config\.", r"^playwright\.config\.",
    r"^cypress\.config\.", r"^\.gitlab-ci\.yml$", r"^Jenkinsfile$", r"^Makefile$",
    r"^Procfile$", r"^vercel\.json$", r"^netlify\.toml$", r"^fly\.toml$", r"^render\.yaml$",
    r"^schema\.prisma$", r"^drizzle\.config\.", r"^ormconfig\.", r"^knexfile\.",
    r"^alembic\.ini$", r"^setup\.cfg$", r"^tox\.ini$", r"^pytest\.ini$", r"^\.flake8$",
    r"^ruff\.toml$", r"^mypy\.ini$", r"^checkstyle.*\.xml$", r"^\.gitattributes$",
    r"^\.gitleaks", r"^gitleaks\.toml$", r"^\.pre-commit-config\.yaml$", r"^lefthook\.yml$",
    r"^renovate\.json$", r"^\.mcp\.json$", r"^CLAUDE\.md$", r"^AGENTS\.md$", r"^GEMINI\.md$",
    r"^skaffold\.ya?ml$", r"^Chart\.yaml$", r"^values.*\.ya?ml$", r"^kustomization\.ya?ml$",
]
CONFIG_DIRS = {".github", ".husky", ".vscode", ".claude", ".cursor", ".devcontainer", "k8s", ".circleci"}

ENTRY_NAMES = {
    "main.ts", "main.tsx", "main.js", "main.jsx", "index.ts", "index.tsx", "index.js",
    "server.ts", "server.js", "app.ts", "app.js", "App.tsx", "App.jsx", "App.vue",
    "main.py", "app.py", "manage.py", "wsgi.py", "asgi.py", "__main__.py", "main.go",
    "Program.cs", "main.rs", "index.html",
}

DOC_PATTERNS = [
    r"^README", r"^CHANGELOG", r"^ROADMAP", r"^CONTRIBUTING", r"^TODO", r"^PLAN",
    r"^ARCHITECTURE", r"^DESIGN", r"^CLAUDE\.md$", r"^AGENTS\.md$",
]

SPEC_DIRS = {"openspec", "specs", "spec", "requirements", "rfcs", "rfc", "adr", "adrs",
             "decisions", "design", "docs", "doc", "documentation", "blueprint", "proposals"}
SPEC_NAME_RE = re.compile(
    r"(prd|srs|brd|requirement|specification|user[-_ ]?stor|use[-_ ]?case|proposal|design|"
    r"blueprint|architecture|roadmap|timeline|tasks|adr[-_]?\d|rfc[-_]?\d|đặc[-_ ]?tả|dac[-_ ]?ta|yeu[-_ ]?cau)",
    re.I)
API_SPEC_RE = re.compile(r"^(openapi|swagger|asyncapi)[\w.-]*\.(ya?ml|json)$", re.I)
DOC_BIN_EXTS = {".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".csv"}
TEST_SPEC_RE = re.compile(r"\.(spec|test)\.[jt]sx?$|Spec\.(java|kt|groovy|scala)$|_spec\.rb$", re.I)


def find_specs(files: list[Path]) -> dict[str, list[Path]]:
    """Gom file đặc tả theo nhóm; bỏ qua file test kiểu *.spec.ts."""
    groups: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        if TEST_SPEC_RE.search(f.name):
            continue
        low_parts = [p.lower() for p in f.parts[:-1]]
        in_spec_dir = any(p in SPEC_DIRS for p in low_parts)
        ext = f.suffix.lower()
        if API_SPEC_RE.match(f.name) or ext in (".proto", ".graphql", ".gql"):
            groups["Đặc tả API / hợp đồng"].append(f)
        elif ext == ".feature":
            groups["Đặc tả hành vi (Gherkin)"].append(f)
        elif "openspec" in low_parts:
            sub = "changes (đang làm/đề xuất)" if "changes" in low_parts and "archive" not in low_parts else \
                  "archive (đã xong)" if "archive" in low_parts else "specs (hiện hành)"
            groups[f"openspec — {sub}"].append(f)
        elif ext in DOC_BIN_EXTS and (in_spec_dir or SPEC_NAME_RE.search(f.stem)):
            groups["Tài liệu Word/PDF/bảng tính"].append(f)
        elif ext in (".md", ".mdx", ".rst", ".txt", ".adoc") and (
                SPEC_NAME_RE.search(f.stem) or (in_spec_dir and "node_modules" not in low_parts)):
            groups["Đặc tả / thiết kế / kế hoạch"].append(f)
    return groups


MARKER_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
TEXT_EXTS = set(LANG_BY_EXT) | {".md", ".yml", ".yaml", ".json", ".toml", ".xml", ".properties", ".txt"}


def run_git(root: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def list_files(root: Path) -> list[Path]:
    """Ưu tiên git ls-files (tôn trọng .gitignore); nếu không có git thì tự duyệt."""
    out = run_git(root, "ls-files", "-co", "--exclude-standard")
    if out:
        files = []
        for line in out.splitlines():
            p = Path(line)
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if (root / p).is_file():
                files.append(p)
        return files
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel = Path(dirpath).relative_to(root)
        files.extend(rel / f for f in filenames)
    return files


def build_tree(files: list[Path], max_depth: int) -> list[str]:
    counts: dict[tuple[str, ...], int] = Counter()
    for f in files:
        parts = f.parts[:-1]
        for i in range(1, min(len(parts), max_depth) + 1):
            counts[parts[:i]] += 1
    lines = []
    for key in sorted(counts):
        depth = len(key)
        lines.append(f"{'  ' * (depth - 1)}- {key[-1]}/  ({counts[key]} file)")
    top_files = sorted(str(f) for f in files if len(f.parts) == 1)
    return lines + [f"- {f}" for f in top_files]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-tree-depth", type=int, default=3)
    ap.add_argument("--max-tree-lines", type=int, default=150)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Không tìm thấy thư mục: {root}", file=sys.stderr)
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    files = list_files(root)
    print(f"# Kết quả quét: {root.name}\n")
    print(f"Tổng số file (bỏ qua thư mục build/deps): **{len(files)}**\n")

    # Manifest
    print("## Manifest & stack đoán được\n")
    manifests = [f for f in files if f.name in MANIFESTS or f.suffix in (".csproj", ".sln")]
    if manifests:
        for f in sorted(manifests, key=lambda p: (len(p.parts), str(p)))[:60]:
            kind = MANIFESTS.get(f.name, "C#/.NET")
            print(f"- `{f.as_posix()}` — {kind}")
        if len(manifests) > 60:
            print(f"- ... và {len(manifests) - 60} manifest khác")
    else:
        print("- (không thấy manifest quen thuộc)")
    print()

    # Languages
    print("## Số file theo ngôn ngữ\n")
    langs = Counter(LANG_BY_EXT[f.suffix.lower()] for f in files if f.suffix.lower() in LANG_BY_EXT)
    print("| Ngôn ngữ | Số file |\n|---|---|")
    for lang, n in langs.most_common(15):
        print(f"| {lang} | {n} |")
    print()

    # Tree
    print(f"## Cây thư mục (tối đa {args.max_tree_depth} cấp)\n")
    tree = build_tree(files, args.max_tree_depth)
    for line in tree[: args.max_tree_lines]:
        print(line)
    if len(tree) > args.max_tree_lines:
        print(f"... (cắt bớt {len(tree) - args.max_tree_lines} dòng; tăng --max-tree-lines nếu cần)")
    print()

    # Docs
    print("## Tài liệu có sẵn\n")
    doc_exts = {".md", ".mdx", ".rst", ".txt", ".adoc", ""}
    docs = [f for f in files if f.suffix.lower() in doc_exts and (
            any(re.match(p, f.name, re.I) for p in DOC_PATTERNS)
            or (f.parts and f.parts[0].lower() in ("docs", "doc", "adr") and f.suffix == ".md"))]
    for f in sorted(docs, key=lambda p: (len(p.parts), str(p)))[:40]:
        print(f"- `{f.as_posix()}`")
    if not docs:
        print("- (không có)")
    print()

    # Specs
    print("## Đặc tả & tài liệu thiết kế\n")
    specs = find_specs(files)
    # openspec: gom theo từng change, đếm checkbox trong tasks.md để thấy tiến độ
    changes: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for group in [g for g in specs if g.startswith("openspec") and "specs (hiện hành)" not in g]:
        for f in specs.pop(group):
            parts = [p.lower() for p in f.parts]
            i = parts.index("changes") if "changes" in parts else -1
            if i < 0 or i + 1 >= len(f.parts) - 1:
                continue
            j = i + 2 if f.parts[i + 1].lower() == "archive" else i + 1
            if j < len(f.parts) - 1:
                changes[("đã archive" if j == i + 2 else "đang mở", f.parts[j])].append(f)
    if changes:
        print("**openspec changes** (trạng thái | change | tiến độ tasks.md)")
        def unchecked(fs):
            t = next((f for f in fs if f.name == "tasks.md"), None)
            if not t:
                return 0
            return len(re.findall(r"- \[ \]", (root / t).read_text(encoding="utf-8", errors="ignore")))

        opened = sorted(k for k in changes if k[0] == "đang mở")
        archived = sorted(k for k in changes if k[0] != "đang mở")
        if len(archived) > 10:
            # Luôn giữ change đã archive mà còn task chưa tick — dấu hiệu việc bị bỏ dở
            leftover = [k for k in archived[:-10] if unchecked(changes[k])]
            print(f"- ({len(archived)} change đã archive; hiện 10 change gần nhất"
                  + (f" + {len(leftover)} change cũ còn task chưa tick)" if leftover else ")"))
            archived = leftover + archived[-10:]
        for key in opened + archived:
            (state, name), fs = key, changes[key]
            tasks = next((f for f in fs if f.name == "tasks.md"), None)
            prog = ""
            if tasks:
                t = (root / tasks).read_text(encoding="utf-8", errors="ignore")
                done, todo = len(re.findall(r"- \[[xX]\]", t)), len(re.findall(r"- \[ \]", t))
                prog = f"{done}/{done + todo} task xong" if done + todo else "không có checkbox"
            loc = tasks.parent.as_posix() if tasks else fs[0].parent.as_posix()
            print(f"- {state} | `{name}` | {prog or 'không có tasks.md'} | `{loc}/`")
        print()
    if specs:
        for group in sorted(specs):
            items = sorted(specs[group], key=lambda p: (len(p.parts), str(p)))
            print(f"**{group}** ({len(items)} file)")
            for f in items[:25]:
                print(f"- `{f.as_posix()}`")
            if len(items) > 25:
                print(f"- ... và {len(items) - 25} file khác")
            print()
    elif not changes:
        print("- (không tìm thấy đặc tả — nghiệp vụ sẽ phải suy ra từ code, test, UI)\n")

    # Config files
    print("## File cấu hình & file đặc biệt\n")
    cfg = [f for f in files if any(re.match(p, f.name) for p in CONFIG_PATTERNS)
           or (f.parts and f.parts[0] in CONFIG_DIRS)]
    by_dir: dict[str, list[str]] = defaultdict(list)
    for f in cfg:
        by_dir[f.parent.as_posix()].append(f.name)
    shown = 0
    for d in sorted(by_dir, key=lambda x: (x.count("/"), x)):
        if shown >= 50:
            print(f"- ... và {len(by_dir) - shown} thư mục khác")
            break
        names = sorted(by_dir[d])
        extra = f" (+{len(names) - 12})" if len(names) > 12 else ""
        print(f"- `{d}/`: {', '.join(names[:12])}{extra}")
        shown += 1
    # File .env thật thường bị gitignore nên git ls-files không thấy — tìm trực tiếp trên đĩa (chỉ tên, không đọc giá trị)
    env_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        dirnames[:] = [] if len(rel.parts) >= 4 else [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == ".env" or (fn.startswith(".env.") and not re.search(r"example|sample|template", fn)):
                env_files.append((rel / fn).as_posix())
    if env_files:
        print(f"\n> File môi trường thật (có thể chứa bí mật): {', '.join(f'`{e}`' for e in sorted(env_files))}")
        print("> Chỉ ghi TÊN biến vào tài liệu, KHÔNG chép giá trị.")
    print()

    # Entry points
    print("## Ứng viên entry point\n")
    entries = [f for f in files if f.name in ENTRY_NAMES and len(f.parts) <= 5]
    java_mains = []
    for f in files:
        if f.suffix in (".java", ".kt") and len(java_mains) < 40:
            try:
                txt = (root / f).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "@SpringBootApplication" in txt or "static void main(" in txt:
                java_mains.append(f)
    for f in sorted(entries + java_mains, key=lambda p: (len(p.parts), str(p)))[:40]:
        print(f"- `{f.as_posix()}`")
    if not entries and not java_mains:
        print("- (không tìm thấy — xem `scripts`/`main` trong manifest, Dockerfile CMD)")
    print()

    # Markers
    print("## TODO / FIXME / HACK\n")
    marker_count: Counter = Counter()
    samples: list[str] = []
    for f in files:
        if f.suffix.lower() not in TEXT_EXTS or f.parts[0] in ("docs",):
            continue
        p = root / f
        try:
            if p.stat().st_size > 1_000_000:
                continue
            with p.open(encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    m = MARKER_RE.search(line)
                    if m:
                        marker_count[m.group(1)] += 1
                        if len(samples) < 30:
                            samples.append(f"- `{f.as_posix()}:{i}` {line.strip()[:120]}")
        except OSError:
            continue
    if marker_count:
        print(", ".join(f"{k}: {v}" for k, v in marker_count.most_common()))
        print("\nVí dụ (tối đa 30):")
        print("\n".join(samples))
    else:
        print("- (không có)")
    print()

    # Git
    print("## Git\n")
    head = run_git(root, "rev-parse", "--short", "HEAD")
    if head is None:
        print("- Không phải git repo (hoặc không có git).")
        return 0
    branch = (run_git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip()
    print(f"- Commit hiện tại: `{head.strip()}` trên branch `{branch}`")
    count = (run_git(root, "rev-list", "--count", "HEAD") or "").strip()
    first = (run_git(root, "log", "--reverse", "--format=%ad", "--date=short") or "").splitlines()
    last = (run_git(root, "log", "-1", "--format=%ad", "--date=short") or "").strip()
    print(f"- Số commit: {count}; commit đầu: {first[0] if first else '?'}; commit cuối: {last}")
    branches = (run_git(root, "branch", "-a", "--format=%(refname:short)") or "").split()
    print(f"- Branch ({len(branches)}): {', '.join(branches[:20])}{' ...' if len(branches) > 20 else ''}")
    # Branch hiện tại có đang chậm hơn remote/branch khác không — tránh phân tích code cũ mà không biết
    ab = run_git(root, "rev-list", "--left-right", "--count", "HEAD...@{u}")
    if ab:
        ahead, behind = ab.split()
        print(f"- So với upstream: nhanh hơn {ahead}, chậm hơn {behind} commit"
              + (" ⚠ branch local đang CŨ hơn remote" if int(behind) else ""))
    head_time = int((run_git(root, "log", "-1", "--format=%ct") or "0").strip() or 0)
    refs = run_git(root, "for-each-ref", "--sort=-committerdate", "--count=8",
                   "--format=%(committerdate:unix) %(committerdate:short) %(refname:short)",
                   "refs/heads", "refs/remotes") or ""
    newer = [l.split(" ", 2) for l in refs.splitlines() if l.strip()]
    newer = [(d, n) for t, d, n in newer if int(t) > head_time and n not in (branch, "origin/HEAD", "origin")]
    if newer:
        print("- ⚠ Branch có commit MỚI hơn HEAD: " + ", ".join(f"`{n}` ({d})" for d, n in newer[:6])
              + " — cân nhắc phân tích branch đó hoặc ghi chú trong phần 12")
    status = run_git(root, "status", "--porcelain") or ""
    print(f"- Thay đổi chưa commit: {len(status.splitlines())} file")
    print("\n### 20 commit gần nhất\n")
    log = run_git(root, "log", "-20", "--format=%h %ad %s", "--date=short") or ""
    for line in log.splitlines():
        print(f"- {line}")
    print("\n### File thay đổi nhiều nhất (200 commit gần nhất)\n")
    churn = run_git(root, "log", "-200", "--name-only", "--format=") or ""
    # Chỉ giữ file còn tồn tại (bỏ đường dẫn cũ trước khi đổi tên)
    c = Counter(l for l in churn.splitlines() if l.strip() and not any(s in l for s in ("lock", "node_modules"))
                and (root / l).is_file())
    for name, n in c.most_common(15):
        print(f"- `{name}` — {n} lần")
    return 0


if __name__ == "__main__":
    sys.exit(main())
