# PDF to Markdown Skill

一个用于将本地 PDF 转成 Markdown 的 Codex skill。转换结果带 PDF 页码标记，默认将图片保存到 Markdown 旁边的文件夹。支持可提取文本的 PDF，也可在安装 OCR 引擎后处理扫描页。

## 安装

将 [`pdf-to-markdown/`](pdf-to-markdown/) 文件夹复制到 Codex 的 skills 目录（通常是 `~/.codex/skills/`），再在运行脚本的 Python 环境里安装依赖：

```bash
python -m pip install -r pdf-to-markdown/requirements.txt
```

扫描件需要本机有可用的 OCR 引擎及对应语言数据。PyMuPDF4LLM 的 [OCR 文档](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/ocr-plugins.html)说明了支持的引擎。缺少 OCR 时，脚本会提示需要检查的空白页；整个文档都提取为空时会报错。

## 使用

在 Codex 中说“用 pdf-to-markdown 把这份 PDF 转成 Markdown”，或直接运行：

```bash
python pdf-to-markdown/scripts/convert.py input.pdf -o output.md
```

常用选项：

```bash
python pdf-to-markdown/scripts/convert.py scan.pdf -o scan.md --ocr-language chi_sim+eng
python pdf-to-markdown/scripts/convert.py input.pdf -o output.md --no-images
python pdf-to-markdown/scripts/convert.py input.pdf -o output.md --overwrite
```

`--force-ocr` 仅适用于文本层损坏的 PDF；普通文本 PDF 使用自动判断即可。转换后应将 Markdown 与原 PDF 对照检查，特别是表格、公式、图注和多栏阅读顺序。

转换引擎：[PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm)。
