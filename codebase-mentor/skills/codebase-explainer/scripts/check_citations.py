#!/usr/bin/env python3
"""Kiểm tra dẫn chứng `file:dòng` trong tài liệu do codebase-explainer viết.

Cách dùng:
    python check_citations.py <thư-mục-tài-liệu> <gốc-repo> [--fix]

Tìm mọi đoạn trong backtick dạng `đường/dẫn/file.ext:12`, `file.ext:12-30`,
`file.ext:12,40-45` (và comment `// file.ext:12-30` ở dòng đầu block code), rồi:
- kiểm tra file tồn tại (đường dẫn tương đối từ gốc repo; tên ngắn được chấp nhận
  nếu khớp DUY NHẤT một file trong repo, mơ hồ thì báo lỗi; dạng viết tắt
  `order/.../X.java` bị báo kèm đường dẫn đầy đủ, `--fix` tự thay khi đích là duy nhất);
- kiểm tra mọi vùng dòng nằm trong độ dài file;
- với block code có ghi vị trí: so nội dung block với file quanh vùng dòng đó
  (bỏ qua khoảng trắng; dòng có "..." coi là đã lược; block ghi "(rút gọn)" thì bỏ qua).
Thoát mã 1 nếu có dẫn chứng hỏng hoặc block nghi không khớp.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

RANGES = r"\d+(?:-\d+)?(?:,\s?\d+(?:-\d+)?)*"
CITE_RE = re.compile(rf"(?P<path>[\w./\\@\-\[\]()+ ]*?\.[A-Za-z0-9]+):(?P<ranges>{RANGES})")
INLINE_RE = re.compile(r"`([^`\n]+)`")
COMMENT_RE = re.compile(rf"^\s*(?://|#|--|<!--|/\*|;|')\s*(\S+:{RANGES})")
HOST_RE = re.compile(r"^(\d{1,3}(\.\d{1,3}){3}|localhost|[\w-]+(\.[\w-]+)*\."
                     r"(com|net|org|io|local|online|dev|app|vn|ai|co))$", re.I)
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "target", ".next"}


class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.by_name: dict[str, list[str]] = defaultdict(list)
        self._lines: dict[Path, list[str]] = {}
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            rel = Path(dirpath).relative_to(root)
            for fn in filenames:
                self.by_name[fn].append((rel / fn).as_posix())

    def resolve(self, raw: str) -> tuple[Path | None, str]:
        raw = raw.strip().replace("\\", "/")
        while raw.startswith("./"):
            raw = raw[2:]
        cand = self.root / raw
        if cand.is_file():
            return cand, ""
        hits = self.candidates(raw)
        if len(hits) == 1 and "..." not in raw and "…" not in raw:
            return self.root / hits[0], ""  # tên ngắn khớp duy nhất — chấp nhận
        if len(hits) == 1:
            return None, f"viết tắt — dùng `{hits[0]}`"
        if len(hits) > 1:
            return None, f"mơ hồ, khớp {len(hits)} file (vd. {', '.join(hits[:3])}) — ghi đường dẫn đầy đủ"
        return None, "không có file"

    def candidates(self, raw: str) -> list[str]:
        """File có thể là đích của một dẫn chứng tên ngắn hoặc viết tắt kiểu `order/.../X.java`."""
        name = Path(raw.replace("…", "...")).name
        pool = self.by_name.get(name, [])
        if "..." in raw or "…" in raw:
            head, _, tail = raw.replace("…", "...").partition("...")
            head, tail = head.strip("/"), tail.strip("/")
            return [p for p in pool if (not head or p.startswith(head + "/")) and p.endswith(tail)]
        return [p for p in pool if p == raw or p.endswith("/" + raw)]

    def lines(self, p: Path) -> list[str]:
        if p not in self._lines:
            self._lines[p] = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        return self._lines[p]


def parse_ranges(s: str) -> list[tuple[int, int]]:
    out = []
    for part in s.replace(" ", "").split(","):
        a, _, b = part.partition("-")
        out.append((int(a), int(b) if b else int(a)))
    return out


def block_ratio(lines: list[str], ranges: list[tuple[int, int]], body: list[str]) -> float:
    """Tỉ lệ dòng trong block code tìm thấy trong file quanh các vùng dòng đã ghi."""
    window = "".join(
        re.sub(r"\s+", "", "".join(lines[max(0, a - 4): b + 3])) for a, b in ranges)
    wanted = [re.sub(r"\s+", "", l) for l in body]
    wanted = [w for w in wanted if w and "..." not in w and "…" not in w]
    if not wanted:
        return 1.0
    return sum(w in window for w in wanted) / len(wanted)


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--fix"]
    do_fix = "--fix" in sys.argv[1:]
    if len(args) != 2:
        print(__doc__)
        return 2
    docs, root = Path(args[0]), Path(args[1]).resolve()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    repo = Repo(root)
    fixes: dict[str, list[tuple[str, str]]] = {}
    total = blocks_checked = 0
    problems: list[str] = []
    warnings: list[str] = []

    def check(text: str, where: str):
        """Trả về (file, ranges) của dẫn chứng hợp lệ cuối cùng trong text, để so block code."""
        nonlocal total
        last = None
        for m in CITE_RE.finditer(text):
            path = m.group("path")
            if "://" in text or HOST_RE.match(path.strip()):
                continue
            total += 1
            target, why = repo.resolve(path)
            if target is None:
                tag = "KHÔNG CÓ FILE" if why == "không có file" else "VIẾT TẮT" if why.startswith("viết tắt") else "MƠ HỒ"
                problems.append(f"[{tag}] {where} → `{m.group(0)}`" + ("" if tag == "KHÔNG CÓ FILE" else f" ({why})"))
                if tag == "VIẾT TẮT":
                    fixes.setdefault(where.rsplit(":", 1)[0], []).append((path, why.split("`")[1]))
                continue
            n = len(repo.lines(target))
            rs = parse_ranges(m.group("ranges"))
            badr = [f"{a}-{b}" if a != b else str(a) for a, b in rs if a < 1 or b < a or b > n]
            if badr:
                problems.append(f"[SAI DÒNG] {where} → `{m.group(0)}` (file có {n} dòng; vùng sai: {', '.join(badr)})")
            else:
                last = (target, rs, m.group(0))
        return last

    for md in sorted(docs.rglob("*.md")):
        lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
        in_code, lang, cite, body = False, "", None, []
        for ln, line in enumerate(lines, 1):
            where = f"{md.relative_to(docs).as_posix()}:{ln}"
            if line.lstrip().startswith("```"):
                if in_code and cite and lang != "mermaid":
                    target, rs, label, w0 = cite
                    blocks_checked += 1
                    ratio = block_ratio(repo.lines(target), rs, body)
                    if ratio < 0.6:
                        warnings.append(f"[CODE KHÔNG KHỚP {ratio:.0%}] {w0} → `{label}` — code trích không giống "
                                        "nội dung file ở vùng dòng này (nếu cố ý rút gọn, ghi '(rút gọn)' ở dòng vị trí)")
                in_code = not in_code
                lang = line.strip()[3:].strip().lower() if in_code else ""
                cite, body = None, []
                continue
            if not in_code:
                for t in INLINE_RE.findall(line):
                    check(t, where)
                continue
            m = COMMENT_RE.match(line)
            if m and not body and cite is None:
                found = check(m.group(1), where)
                low = line.lower()
                if found and "rút gọn" not in low and "viết lại" not in low:
                    cite = (*found, where)
                elif found:
                    body.append("...")
            else:
                body.append(line)

    if do_fix and fixes:
        n = 0
        for rel, pairs in fixes.items():
            f = docs / rel
            t = f.read_text(encoding="utf-8")
            for short, full in set(pairs):
                c = t.count(short + ":")
                t = t.replace(short + ":", full + ":")
                n += c
            f.write_text(t, encoding="utf-8")
        print(f"--fix: đã thay {n} dẫn chứng viết tắt bằng đường dẫn đầy đủ. Chạy lại để kiểm tra.")
    elif fixes:
        print(f"Gợi ý: {sum(len(v) for v in fixes.values())} dẫn chứng viết tắt có đích duy nhất — chạy lại với --fix để tự thay.")
    print(f"Đã kiểm tra {total} dẫn chứng, {len(problems)} hỏng. "
          f"Đã so nội dung {blocks_checked} block code, {len(warnings)} block nghi không khớp.")
    for p in problems + warnings:
        print(p)
    return 1 if problems or warnings else 0


if __name__ == "__main__":
    sys.exit(main())
