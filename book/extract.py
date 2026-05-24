#!/usr/bin/env python3
"""Extract memoir chapter content from old hexo HTML files into clean markdown."""
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

RAW = Path("/tmp/memoir_raw")
OUT = Path("/home/user/blog/book/src")
OUT.mkdir(parents=True, exist_ok=True)

# (source filename without .html, ordered output filename, chapter label, chapter title)
CHAPTERS = [
    ("0_auto0",   "00-preface-original", None,        "原序"),
    ("16_auto12", "01-chronology",       None,        "陈炳林 年表"),
    ("10_auto1",  "02-chapter-1",        "第一章",     "我的童年"),
    ("11_auto2",  "03-chapter-2",        "第二章",     "初中生活"),
    ("9_auto3",   "04-chapter-3",        "第三章",     "难忘的一九五八"),
    ("7_auto4",   "05-chapter-4",        "第四章",     "新的篇章"),
    ("8_auto5",   "06-chapter-5",        "第五章",     "休学的日子"),
    ("6_auto6",   "07-chapter-6",        "第六章",     "婚后的生活"),
    ("5_auto7",   "08-chapter-7",        "第七章",     "喜上加喜  喜中有忧"),
    ("4_auto8",   "09-chapter-8",        "第八章",     "工作，崭新的篇章"),
    ("2_auto10",  "10-appendix-poems",   "附录一",     "童年的诗"),
    ("1_auto11",  "11-appendix-justice", "附录二",     "关于正义的故事"),
    ("3_auto9",   "12-appendix-essays",  "附录三",     "短文数篇"),
]


def extract_article(html: str) -> BeautifulSoup:
    """Find the post body within the hexo NexT template."""
    soup = BeautifulSoup(html, "lxml")
    # Hexo NexT puts the body inside <div class="post-body">
    body = soup.select_one("div.post-body")
    if body is None:
        # fallback
        body = soup.select_one("article") or soup
    return body


def clean_node(node):
    """Strip junk elements that don't belong in the print book."""
    for sel in [
        ".post-copyright", ".post-tags", ".post-nav", ".post-related",
        ".post-meta", ".comments", "#comments", "script", "style",
        ".tabs", ".note", "a.headerlink", ".reward-container",
    ]:
        for tag in node.select(sel):
            tag.decompose()


IMG_RE = re.compile(r"\.(jpg|jpeg|png|gif|webp|bmp)(\?|$)", re.IGNORECASE)


def node_to_markdown(node, image_dir: Path, slug: str) -> str:
    """Convert the cleaned article body to markdown, with images replaced by
    placeholders we can later swap for real files."""
    out_lines = []
    img_counter = [0]

    def render(el, indent=0):
        if isinstance(el, NavigableString):
            text = str(el)
            return text
        if not getattr(el, "name", None):
            return ""
        name = el.name
        if name in ("script", "style"):
            return ""
        if name == "h1":
            return f"\n\n# {el.get_text(strip=True)}\n\n"
        if name == "h2":
            return f"\n\n## {el.get_text(strip=True)}\n\n"
        if name == "h3":
            return f"\n\n### {el.get_text(strip=True)}\n\n"
        if name == "h4":
            return f"\n\n#### {el.get_text(strip=True)}\n\n"
        if name == "p":
            inner = "".join(render(c) for c in el.children).strip()
            if not inner:
                return ""
            return f"\n\n{inner}\n\n"
        if name == "br":
            return "  \n"
        if name == "strong" or name == "b":
            return f"**{''.join(render(c) for c in el.children)}**"
        if name == "em" or name == "i":
            return f"*{''.join(render(c) for c in el.children)}*"
        if name == "blockquote":
            inner = "".join(render(c) for c in el.children).strip()
            quoted = "\n".join("> " + ln for ln in inner.splitlines())
            return f"\n\n{quoted}\n\n"
        if name == "ul":
            items = []
            for li in el.find_all("li", recursive=False):
                items.append("- " + "".join(render(c) for c in li.children).strip())
            return "\n\n" + "\n".join(items) + "\n\n"
        if name == "ol":
            items = []
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                items.append(f"{i}. " + "".join(render(c) for c in li.children).strip())
            return "\n\n" + "\n".join(items) + "\n\n"
        if name == "a":
            txt = "".join(render(c) for c in el.children)
            href = el.get("href", "")
            if not href or href.startswith("#"):
                return txt
            return f"[{txt}]({href})"
        if name == "img":
            img_counter[0] += 1
            src = el.get("src", "")
            alt = el.get("alt", "") or ""
            # remote URL — record as placeholder for now
            placeholder = f"{slug}-img{img_counter[0]:02d}.jpg"
            # write a sidecar manifest entry by appending to a list later via
            # closure-attached attribute
            IMG_MANIFEST.append((slug, img_counter[0], src, placeholder))
            return f"\n\n![{alt}](images/{placeholder})\n\n"
        if name == "hr":
            return "\n\n---\n\n"
        if name == "code":
            return f"`{el.get_text()}`"
        # default: recurse
        return "".join(render(c) for c in el.children)

    md = render(node)
    # collapse triple+ blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


IMG_MANIFEST = []  # (slug, idx, original_url, placeholder_filename)


def main():
    manifest_lines = ["# Image manifest\n\nThese are images referenced from the original posts. They live on remote hosts (mostly tiimg.com) that may be defunct. The placeholders point to filenames inside `book/images/`; drop the matching files there (or replace the references) before final typeset.\n\n| Chapter | # | Original URL | Local filename |\n|---|---|---|---|"]
    for src_name, out_name, label, title in CHAPTERS:
        html = (RAW / f"{src_name}.html").read_text(encoding="utf-8", errors="ignore")
        body = extract_article(html)
        clean_node(body)
        md = node_to_markdown(body, OUT.parent / "images", out_name)
        # Header block: keep chapter label + title as YAML-ish front matter
        front = "---\n"
        if label:
            front += f"label: \"{label}\"\n"
        front += f"title: \"{title}\"\n---\n\n"
        (OUT / f"{out_name}.md").write_text(front + md, encoding="utf-8")
        print(f"wrote {out_name}.md  ({len(md):>6} chars)")
    for slug, idx, src, ph in IMG_MANIFEST:
        manifest_lines.append(f"| {slug} | {idx} | {src} | {ph} |")
    (OUT.parent / "images" / "MANIFEST.md").write_text("\n".join(manifest_lines), encoding="utf-8")
    print(f"\nTotal images referenced: {len(IMG_MANIFEST)}")


if __name__ == "__main__":
    main()
