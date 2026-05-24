#!/usr/bin/env python3
"""Convert each chapter markdown into a LaTeX body fragment (no preamble)
for \input{}. Handles paragraphs, bold/italic, lists, blockquotes,
horizontal rules, images, and very simple headers.

Each <slug>.md  ->  <slug>-body.tex
"""
import re
from pathlib import Path

SRC = Path("/home/user/blog/book/src")

# Chapters that should start with \chapter{...}; others (preface, etc.) are
# included as raw bodies.
BODY_CHAPTERS = {
    "02-chapter-1":      ("chapter",        "我的童年"),
    "03-chapter-2":      ("chapter",        "初中生活"),
    "04-chapter-3":      ("chapter",        "难忘的一九五八"),
    "05-chapter-4":      ("chapter",        "新的篇章"),
    "06-chapter-5":      ("chapter",        "休学的日子"),
    "07-chapter-6":      ("chapter",        "婚后的生活"),
    "08-chapter-7":      ("chapter",        "喜上加喜  喜中有忧"),
    "09-chapter-8":      ("chapter",        "工作，崭新的篇章"),
    "10-appendix-poems":   ("chapter",      "童年的诗"),
    "11-appendix-justice": ("chapter",      "关于正义的故事"),
    "12-appendix-essays":  ("chapter",      "短文数篇"),
    "01-chronology":       ("chapter",      "年表"),
}

# These are "raw bodies" — included without a \chapter wrapper because the
# main .tex already supplies one via \chapter*{} for unnumbered front matter.
RAW_BODIES = {
    "00-preface-original",  # 原序
}


def escape_tex(s: str) -> str:
    """Escape LaTeX special chars. Keep backslash last."""
    # we run this on raw text only — markdown markers were already turned
    # into commands.
    return (s.replace("\\", r"\textbackslash{}")
             .replace("&", r"\&")
             .replace("%", r"\%")
             .replace("$", r"\$")
             .replace("#", r"\#")
             .replace("_", r"\_")
             .replace("{", r"\{")
             .replace("}", r"\}")
             .replace("~", r"\textasciitilde{}")
             .replace("^", r"\textasciicircum{}"))


INLINE_PATTERNS = [
    # images come first (so we don't mangle their alt/url)
    (re.compile(r"!\[([^\]]*)\]\(([^\)]+)\)"),
        lambda m: f"\n\n\\begin{{figure}}[!htbp]\\centering\\safeimage{{{m.group(2).split('/')[-1]}}}\\end{{figure}}\n\n"),
    # links — keep just the visible text (no clickable links in print book)
    (re.compile(r"\[([^\]]+)\]\(([^\)]+)\)"),
        lambda m: m.group(1)),
    # bold
    (re.compile(r"\*\*([^*]+)\*\*"),
        lambda m: r"\textbf{" + m.group(1) + "}"),
    # italic
    (re.compile(r"(?<![*_])\*([^*\n]+)\*(?![*_])"),
        lambda m: r"\textit{" + m.group(1) + "}"),
]


def md_inline_to_tex(line: str) -> str:
    """Convert one line of markdown into LaTeX. Order matters: images, links,
    bold, italic — *then* escape remaining text."""
    # We need to escape the plain pieces but leave the commands alone. Do a
    # token-walk: split on the inline patterns greedily.
    # Easiest approach: escape first, then re-apply patterns to the escaped
    # text using the same syntactic markers (since markdown markers don't
    # collide with our escape set).
    s = escape_tex(line)
    for pat, repl in INLINE_PATTERNS:
        s = pat.sub(repl, s)
    return s


def convert_body(md: str) -> str:
    """Convert the markdown body into LaTeX. Skips the YAML front matter."""
    # Strip front matter
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.DOTALL)
    md = md.strip()

    out_lines = []
    blocks = re.split(r"\n\s*\n", md)
    in_list = False
    list_kind = None
    list_buf = []

    def flush_list():
        nonlocal list_buf, in_list, list_kind
        if not list_buf:
            return
        env = "enumerate" if list_kind == "ol" else "itemize"
        out_lines.append("\\begin{" + env + "}[leftmargin=2.5em,itemsep=2pt]")
        for it in list_buf:
            out_lines.append("  \\item " + md_inline_to_tex(it))
        out_lines.append("\\end{" + env + "}")
        list_buf = []
        in_list = False
        list_kind = None

    for blk in blocks:
        blk = blk.strip("\n")
        if not blk.strip():
            continue

        # Headers
        m = re.match(r"^(#{1,4})\s+(.*)$", blk)
        if m:
            flush_list()
            level = len(m.group(1))
            text = md_inline_to_tex(m.group(2).strip())
            if level == 1:
                out_lines.append("\n\\section*{" + text + "}\n")
            elif level == 2:
                out_lines.append("\n\\subsection*{" + text + "}\n")
            else:
                out_lines.append("\n\\subsubsection*{" + text + "}\n")
            continue

        # Horizontal rule -> dinkus
        if re.match(r"^-{3,}\s*$", blk) or re.match(r"^\*{3,}\s*$", blk):
            flush_list()
            out_lines.append("\\dinkus")
            continue

        # Blockquote
        if blk.startswith(">"):
            flush_list()
            inner_lines = [ln.lstrip("> ").rstrip() for ln in blk.splitlines()]
            inner = " ".join(inner_lines).strip()
            out_lines.append("\\begin{quote}" + md_inline_to_tex(inner) + "\\end{quote}")
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", blk):
            flush_list()
            in_list = True
            list_kind = "ul"
            for ln in blk.splitlines():
                m = re.match(r"^[-*]\s+(.*)$", ln)
                if m:
                    list_buf.append(m.group(1).strip())
                else:
                    if list_buf:
                        list_buf[-1] += " " + ln.strip()
            flush_list()
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", blk):
            flush_list()
            in_list = True
            list_kind = "ol"
            for ln in blk.splitlines():
                m = re.match(r"^\d+\.\s+(.*)$", ln)
                if m:
                    list_buf.append(m.group(1).strip())
                else:
                    if list_buf:
                        list_buf[-1] += " " + ln.strip()
            flush_list()
            continue

        # Plain paragraph. Collapse "  \n" (markdown line break) -> space; the
        # original posts used these to keep tight line wrapping but in print
        # we want a flowing paragraph.
        flush_list()
        para = re.sub(r"  \n", " ", blk)
        para = re.sub(r"\n", " ", para)
        para = re.sub(r" {2,}", " ", para).strip()
        out_lines.append(md_inline_to_tex(para))
        out_lines.append("")

    flush_list()
    return "\n".join(out_lines).strip() + "\n"


def main():
    for src_file in sorted(SRC.glob("*.md")):
        stem = src_file.stem
        raw = src_file.read_text(encoding="utf-8")
        body = convert_body(raw)

        if stem in BODY_CHAPTERS:
            kind, title = BODY_CHAPTERS[stem]
            out = f"\\chapter{{{title}}}\n\n{body}\n"
        elif stem in RAW_BODIES:
            out = body
        else:
            # unknown -> treat as raw
            out = body

        out_path = SRC / f"{stem}-body.tex"
        out_path.write_text(out, encoding="utf-8")
        print(f"wrote {out_path.name}  ({len(out):>6} chars)")


if __name__ == "__main__":
    main()
