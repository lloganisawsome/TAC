#!/usr/bin/env python3
"""
Combine subfolder web games into single-file HTML pages.
Updated: Added cycle detection to prevent infinite recursion.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import re
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR / "files"

TEXT_EXTENSIONS = {".css", ".html", ".js", ".json", ".mjs", ".svg", ".txt", ".xml"}
ASSET_EXTENSIONS = {
    ".avif", ".bmp", ".cur", ".flac", ".gif", ".ico", ".jpeg", ".jpg", ".m4a",
    ".mp3", ".mp4", ".ogg", ".otf", ".png", ".svg", ".swf", ".ttf", ".wav",
    ".wav", ".wasm", ".webm", ".webp", ".woff", ".woff2",
}

SCRIPT_TAG_RE = re.compile(
    r"<script(?P<attrs>[^>]*?)\s+src=(?P<quote>['\"])(?P<path>.*?)(?P=quote)(?P<rest>[^>]*)>\s*</script>",
    re.IGNORECASE | re.DOTALL,
)
STYLESHEET_TAG_RE = re.compile(
    r"<link(?P<attrs>[^>]*?)\s+href=(?P<quote>['\"])(?P<path>.*?)(?P=quote)(?P<rest>[^>]*)>",
    re.IGNORECASE | re.DOTALL,
)
STYLE_IMPORT_RE = re.compile(
    r"@import\s+(?:url\(\s*)?(?P<quote>['\"])(?P<path>.*?)(?P=quote)\s*\)?\s*;",
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(
    r"url\(\s*(?P<quote>['\"]?)(?P<path>.*?)(?P=quote)\s*\)",
    re.IGNORECASE,
)
HTML_ATTR_RE = re.compile(
    r"""(?P<attr>\b(?:src|href|poster|data)\b)\s*=\s*(?P<quote>['"])(?P<path>.*?)(?P=quote)""",
    re.IGNORECASE | re.DOTALL,
)
PARAM_VALUE_RE = re.compile(
    r"""<param(?P<before>[^>]*?\bname\s*=\s*['"](?:movie|src)['"][^>]*?\bvalue\s*=\s*)(?P<quote>['"])(?P<path>.*?)(?P=quote)(?P<after>[^>]*?)>""",
    re.IGNORECASE | re.DOTALL,
)
SOURCE_MAP_RE = re.compile(r"(?m)^[ \t]*//[#@]\s*sourceMappingURL=.*?$")
JS_STRING_RE = re.compile(
    r"""(?P<quote>['"])(?P<path>(?![a-zA-Z][a-zA-Z0-9+.-]*:|//|/|#|\?)[^"'`\s][^"'`]*?\.[a-zA-Z0-9]{2,8}(?:\?[^"'`]*)?(?:#[^"'`]*)?)(?P=quote)"""
)


def strip_attribute(attrs: str, attr_name: str) -> str:
    return re.sub(rf"""\s*\b{re.escape(attr_name)}\s*=\s*(["']).*?\1""", "", attrs, flags=re.IGNORECASE | re.DOTALL)


def strip_rel_stylesheet(attrs: str) -> str:
    return re.sub(r"""\s*\brel\s*=\s*(["'])stylesheet\1""", "", attrs, flags=re.IGNORECASE | re.DOTALL)


def should_inline_path(path_text: str) -> bool:
    if not path_text: return False
    lowered = path_text.lower().strip()
    blocked = ("data:", "http:", "https:", "javascript:", "mailto:", "tel:", "//", "/", "#", "?")
    return not lowered.startswith(blocked)


def split_url_parts(path_text: str) -> tuple[str, str]:
    positions = [i for i in (path_text.find("?"), path_text.find("#")) if i != -1]
    if not positions: return path_text, ""
    cut = min(positions)
    return path_text[:cut], path_text[cut:]


def resolve_local_asset(base_dir: Path, raw_path: str) -> Path | None:
    if not should_inline_path(raw_path): return None
    clean_path, _suffix = split_url_parts(raw_path.strip())
    if not clean_path: return None
    candidate = (base_dir / clean_path).resolve()
    try:
        candidate.relative_to(base_dir.resolve())
    except ValueError:
        return None
    return candidate


def guess_mime_type(path: Path) -> str:
    special = {".js": "application/javascript", ".mjs": "application/javascript", ".wasm": "application/wasm", ".swf": "application/x-shockwave-flash"}
    if path.suffix.lower() in special: return special[path.suffix.lower()]
    mime_type, _ = mimetypes.guess_type(path.name)
    return mime_type or "application/octet-stream"


def to_data_uri(data: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64.b64encode(data).decode('ascii')}"


class Inliner:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.cache: dict[Path, str] = {}
        # Track stack to prevent infinite recursion
        self._visiting: set[Path] = set()

    def log(self, message: str) -> None:
        if self.verbose: print(message)

    def data_uri_for_path(self, asset_path: Path) -> str:
        if asset_path in self.cache: return self.cache[asset_path]
        data_uri = to_data_uri(asset_path.read_bytes(), guess_mime_type(asset_path))
        self.cache[asset_path] = data_uri
        self.log(f"Inlining asset: {asset_path}")
        return data_uri

    def inline_html_file(self, html_path: Path) -> str:
        html = html_path.read_text(encoding="utf-8", errors="replace")
        return self.inline_html_text(html, html_path.parent)

    def inline_html_text(self, html: str, base_dir: Path) -> str:
        html = SCRIPT_TAG_RE.sub(lambda m: self.replace_script_tag(m, base_dir), html)
        html = STYLESHEET_TAG_RE.sub(lambda m: self.replace_stylesheet_tag(m, base_dir), html)
        html = PARAM_VALUE_RE.sub(lambda m: self.replace_param_value(m, base_dir), html)
        html = HTML_ATTR_RE.sub(lambda m: self.replace_html_attr(m, base_dir), html)
        return html

    def inline_css_text(self, css: str, base_dir: Path) -> str:
        css = STYLE_IMPORT_RE.sub(lambda m: self.replace_css_import(m, base_dir), css)
        css = CSS_URL_RE.sub(lambda m: self.replace_css_url(m, base_dir), css)
        return css

    def inline_js_text(self, js: str, base_dir: Path) -> str:
        js = SOURCE_MAP_RE.sub("", js)
        js = JS_STRING_RE.sub(lambda m: self.replace_js_string(m, base_dir), js)
        return js

    def replace_script_tag(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file() or asset_path in self._visiting: return match.group(0)
        
        self._visiting.add(asset_path)
        script_text = asset_path.read_text(encoding="utf-8", errors="replace")
        script_text = self.inline_js_text(script_text, asset_path.parent)
        self._visiting.remove(asset_path)
        
        attrs = strip_attribute(match.group("attrs") + match.group("rest"), "src").strip()
        attr_text = f" {attrs}" if attrs else ""
        return f"<script{attr_text}>\n{script_text}\n</script>"

    def replace_stylesheet_tag(self, match: re.Match[str], base_dir: Path) -> str:
        if "stylesheet" not in match.group(0).lower(): return match.group(0)
        source = match.group("path").strip()
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file() or asset_path in self._visiting: return match.group(0)
        
        self._visiting.add(asset_path)
        css_text = asset_path.read_text(encoding="utf-8", errors="replace")
        css_text = self.inline_css_text(css_text, asset_path.parent)
        self._visiting.remove(asset_path)
        
        attrs = strip_rel_stylesheet(strip_attribute(match.group("attrs") + match.group("rest"), "href")).strip()
        attr_text = f" {attrs}" if attrs else ""
        return f"<style{attr_text}>\n{css_text}\n</style>"

    def replace_param_value(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file(): return match.group(0)
        data_uri = self.data_uri_for_path(asset_path)
        return f"<param{match.group('before')}{match.group('quote')}{data_uri}{match.group('quote')}{match.group('after')}>"

    def replace_html_attr(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        if not should_inline_path(source): return match.group(0)
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file(): return match.group(0)
        data_uri = self.data_uri_for_path(asset_path)
        return f'{match.group("attr")}={match.group("quote")}{data_uri}{match.group("quote")}'

    def replace_css_import(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file() or asset_path.suffix.lower() != ".css" or asset_path in self._visiting:
            return match.group(0)
        
        self._visiting.add(asset_path)
        nested_css = asset_path.read_text(encoding="utf-8", errors="replace")
        nested_css = self.inline_css_text(nested_css, asset_path.parent)
        self._visiting.remove(asset_path)
        return f"\n/* inlined from {source} */\n{nested_css}\n"

    def replace_css_url(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        if not should_inline_path(source): return match.group(0)
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file(): return match.group(0)
        return f'url("{self.data_uri_for_path(asset_path)}")'

    def replace_js_string(self, match: re.Match[str], base_dir: Path) -> str:
        source = match.group("path").strip()
        asset_path = resolve_local_asset(base_dir, source)
        if not asset_path or not asset_path.is_file() or asset_path in self._visiting:
            return match.group(0)
        
        ext = asset_path.suffix.lower()
        if ext in TEXT_EXTENSIONS:
            self._visiting.add(asset_path)
            text = asset_path.read_text(encoding="utf-8", errors="replace")
            if ext == ".css": text = self.inline_css_text(text, asset_path.parent)
            elif ext in {".js", ".mjs"}: text = self.inline_js_text(text, asset_path.parent)
            elif ext == ".html": text = self.inline_html_text(text, asset_path.parent)
            self._visiting.remove(asset_path)
            
            data_uri = to_data_uri(text.encode("utf-8"), guess_mime_type(asset_path))
            return f'{match.group("quote")}{data_uri}{match.group("quote")}'
            
        if ext in ASSET_EXTENSIONS:
            return f'{match.group("quote")}{self.data_uri_for_path(asset_path)}{match.group("quote")}'
        return match.group(0)


def iter_target_directories(root: Path, include_hidden: bool):
    root = root.resolve()
    for current_root, dir_names, file_names in os.walk(root):
        current_path = Path(current_root)
        if not include_hidden:
            dir_names[:] = [name for name in dir_names if not name.startswith(".")]
        if current_path == root:
            continue
        if "index.html" in file_names:
            yield current_path


def process_directory(directory: Path, output_name: str, in_place: bool, backup_ext: str | None, inliner: Inliner) -> None:
    source_path = directory / "index.html"
    bundled_html = inliner.inline_html_file(source_path)
    destination = source_path if in_place else directory / output_name
    if in_place and backup_ext:
        shutil.copy2(source_path, source_path.with_name(source_path.name + backup_ext))
    destination.write_text(bundled_html, encoding="utf-8")
    print(f"Wrote {destination}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine subfolder index.html files into self-contained HTML files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help="Root directory to scan. Defaults to a 'files' folder next to this script.",
    )
    parser.add_argument(
        "--output-name",
        default="index.inlined.html",
        help="Output filename when not overwriting in place.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite each subfolder's existing index.html.",
    )
    parser.add_argument(
        "--backup-ext",
        default=".bak",
        help="Backup extension for --in-place. Use '' to disable backups.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden folders.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each asset as it is inlined.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Root directory does not exist: {root}")

    inliner = Inliner(verbose=args.verbose)
    targets = list(iter_target_directories(root, args.include_hidden))
    if not targets:
        print("No subfolders with index.html were found.")
        return 0

    for directory in targets:
        process_directory(
            directory=directory,
            output_name=args.output_name,
            in_place=args.in_place,
            backup_ext=args.backup_ext or None,
            inliner=inliner,
        )

    print(f"Processed {len(targets)} subfolder(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
