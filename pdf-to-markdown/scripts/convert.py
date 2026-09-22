#!/usr/bin/env python3
"""Convert one PDF to page-marked Markdown with optional local images."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source PDF")
    parser.add_argument("-o", "--output", type=Path, help="Output Markdown (default: beside PDF)")
    parser.add_argument("--no-images", action="store_true", help="Do not save figures")
    parser.add_argument("--no-page-markers", action="store_true", help="Omit PDF page comments")
    parser.add_argument("--ocr-language", default="eng", help="OCR language codes, e.g. chi_sim+eng")
    ocr = parser.add_mutually_exclusive_group()
    ocr.add_argument("--force-ocr", action="store_true", help="OCR all pages")
    ocr.add_argument("--no-ocr", action="store_true", help="Disable automatic OCR")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing Markdown file")
    return parser.parse_args()


def convert(args: argparse.Namespace) -> tuple[Path, int, list[int]]:
    source = args.input.expanduser().resolve()
    if not source.is_file() or source.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {source}")

    output = (args.output or source.with_suffix(".md")).expanduser().resolve()
    if output.suffix.lower() != ".md":
        raise ValueError("Output filename must end in .md")
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"Output exists: {output} (use --overwrite to replace it)")

    try:
        import pymupdf4llm
    except ImportError as exc:
        raise RuntimeError("Missing pymupdf4llm; install requirements.txt first") from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    image_dir_name = f"{output.stem}_images"
    image_dir = output.parent / image_dir_name
    if not args.no_images and image_dir.exists() and any(image_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(f"Image directory exists: {image_dir} (use --overwrite to reuse it)")

    previous_dir = Path.cwd()
    try:
        os.chdir(output.parent)
        chunks = pymupdf4llm.to_markdown(
            str(source),
            page_chunks=True,
            write_images=not args.no_images,
            image_path=image_dir_name if not args.no_images else "",
            ocr_language=args.ocr_language,
            force_ocr=args.force_ocr,
            use_ocr=not args.no_ocr,
        )
    finally:
        os.chdir(previous_dir)

    if not isinstance(chunks, list) or not chunks:
        raise RuntimeError("Converter returned no pages")

    sections: list[str] = []
    empty_pages: list[int] = []
    for index, chunk in enumerate(chunks, start=1):
        page = chunk.get("metadata", {}).get("page_number", index)
        body = chunk.get("text", "").strip()
        if not body:
            empty_pages.append(page)
        prefix = f"<!-- PDF page {page} -->\n\n" if not args.no_page_markers else ""
        sections.append(prefix + body)

    if len(empty_pages) == len(chunks):
        raise RuntimeError("All pages extracted as empty; check OCR availability or PDF contents")

    markdown = "\n\n".join(sections).rstrip() + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=output.parent,
        prefix=f".{output.stem}.", suffix=".tmp", delete=False,
    ) as handle:
        handle.write(markdown)
        temporary = Path(handle.name)
    try:
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output, len(chunks), empty_pages


def main() -> int:
    args = parse_args()
    try:
        output, count, empty_pages = convert(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output} ({count} PDF pages)")
    if empty_pages:
        print(f"Review empty pages: {', '.join(map(str, empty_pages))}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
