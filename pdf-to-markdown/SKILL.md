---
name: pdf-to-markdown
description: Convert a local PDF into a reviewable Markdown file with page markers and optional extracted images. Use when the user asks to convert or transcribe a PDF to Markdown; do not invoke for ordinary PDF questions that do not need a Markdown deliverable.
---

# PDF to Markdown

Use the bundled `scripts/convert.py` for a first pass. It uses PyMuPDF4LLM for reading order, tables, and automatic OCR when an OCR engine is available. Its output is a draft: PDF layout, equations, scans, and complex tables can still be misread.

## Convert

1. Confirm the PDF exists and choose an output `.md` path. Keep the source PDF intact. If the document is private, keep its output local unless the user has authorized sharing it.
2. Install `requirements.txt` in the Python environment you will run, if needed. For scanned pages, ensure an OCR engine and the relevant language data are installed. The converter reports empty pages so missing OCR is visible.
3. Run the script from the skill directory, or use its absolute path from another directory:

   ```bash
   python scripts/convert.py input.pdf -o output.md
   ```

   Paths may be absolute. By default, figures are saved beside the Markdown in `<output-stem>_images/`, and each page begins with an HTML comment containing its PDF page number. Use `--no-images` for text-only output, `--ocr-language chi_sim+eng` for Chinese and English OCR, or `--force-ocr` only for a damaged text layer. See `python scripts/convert.py --help` for options.

4. Compare the Markdown with the PDF, paying particular attention to page order, headings, tables, equations, footnotes, and figure captions. Inspect the pages reported as empty. Repair material errors in Markdown, and describe any content that cannot be represented faithfully rather than inventing it. Keep page markers when traceability matters.
5. Check that local image links resolve and that the Markdown covers the expected pages. Report any remaining limitations and the output path.

For a folder of PDFs, run the converter once per PDF and give each document its own Markdown and image directory. Do not combine sources unless the user asks for a combined file.
