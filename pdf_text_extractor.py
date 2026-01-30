#!/usr/bin/env python3
"""
PDF文本提取工具 (使用 PyMuPDF + OCR)
从PDF文件中提取文字内容并输出到终端
支持扫描版PDF的OCR识别
"""

import argparse
import sys
from pathlib import Path
from io import BytesIO

try:
    import fitz  # PyMuPDF
except ImportError:
    print("错误: 需要安装 PyMuPDF 库")
    print("请运行: pip install pymupdf")
    sys.exit(1)

# OCR相关库（可选）
OCR_AVAILABLE = False
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    pass


def parse_page_range(page_range_str, total_pages):
    """
    解析页数范围字符串

    Args:
        page_range_str: 页数范围字符串，如 "1-8" 或 "3,4,5,6" 或 "1-3,5,7-9"
        total_pages: PDF总页数

    Returns:
        页码集合（从0开始的索引）
    """
    pages = set()

    if not page_range_str:
        return None

    try:
        # 分割逗号
        parts = page_range_str.split(',')

        for part in parts:
            part = part.strip()

            # 处理范围，如 "1-8"
            if '-' in part:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())

                if start < 1 or end > total_pages:
                    print(f"警告: 页数范围 {start}-{end} 超出有效范围 (1-{total_pages})")
                    start = max(1, start)
                    end = min(total_pages, end)

                if start > end:
                    print(f"警告: 起始页 {start} 大于结束页 {end}，已交换")
                    start, end = end, start

                # 转换为0索引
                pages.update(range(start - 1, end))

            # 处理单个页码
            else:
                page_num = int(part)
                if page_num < 1 or page_num > total_pages:
                    print(f"警告: 页码 {page_num} 超出有效范围 (1-{total_pages})，已忽略")
                    continue
                pages.add(page_num - 1)  # 转换为0索引

        return sorted(pages) if pages else None

    except ValueError as e:
        print(f"错误: 页数范围格式不正确 '{page_range_str}'")
        print("正确格式示例: '1-8' 或 '3,4,5,6' 或 '1-3,5,7-9'")
        sys.exit(1)


def extract_text_with_ocr(page, page_num):
    """
    使用OCR从PDF页面提取文本

    Args:
        page: PDF页面对象
        page_num: 页码

    Returns:
        提取的文本内容
    """
    if not OCR_AVAILABLE:
        return ""

    try:
        # 将PDF页面转换为图片（提高分辨率以改善OCR效果）
        zoom = 2.0  # 放大倍数
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # 转换为PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(BytesIO(img_data))

        # 使用pytesseract进行OCR，支持中英文
        print(f"正在OCR识别第 {page_num + 1} 页...")
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text

    except Exception as e:
        print(f"OCR识别第 {page_num + 1} 页时出错: {e}")
        return ""


def extract_text_from_pdf(pdf_path, preserve_layout=True, use_ocr=False, page_range=None):
    """
    从PDF文件中提取文本内容

    Args:
        pdf_path: PDF文件路径
        preserve_layout: 是否保留文本布局
        use_ocr: 是否使用OCR（针对扫描版PDF）
        page_range: 页数范围字符串，如 "1-8" 或 "3,4,5,6"

    Returns:
        提取的文本内容
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        print(f"PDF总页数: {total_pages}")
        print(f"文件大小: {Path(pdf_path).stat().st_size / 1024:.2f} KB")

        # 解析页数范围
        pages_to_extract = parse_page_range(page_range, total_pages)
        if pages_to_extract:
            print(f"提取页数: {len(pages_to_extract)} 页 ({page_range})")
        else:
            pages_to_extract = range(total_pages)
            print(f"提取页数: 全部 {total_pages} 页")

        if use_ocr and not OCR_AVAILABLE:
            print("警告: OCR功能不可用，请安装依赖: pip install pytesseract pillow")
            print("并安装Tesseract OCR引擎")
            use_ocr = False

        print("=" * 80)

        all_text = []
        empty_pages = 0

        for page_num in pages_to_extract:
            page = doc[page_num]

            # 提取文本
            if preserve_layout:
                text = page.get_text("text")
            else:
                text = page.get_text()

            # 如果没有文本且启用OCR，则尝试OCR识别
            if not text.strip() and use_ocr:
                text = extract_text_with_ocr(page, page_num)

            if text.strip():
                all_text.append(f"\n--- 第 {page_num + 1} 页 ---\n")
                all_text.append(text)
            else:
                empty_pages += 1

        doc.close()

        if empty_pages > 0:
            print(f"\n注意: {empty_pages} 页没有提取到文本")
            if not use_ocr:
                print("提示: 这可能是扫描版PDF，尝试使用 --ocr 参数进行OCR识别")

        return ''.join(all_text)

    except FileNotFoundError:
        print(f"错误: 找不到文件 '{pdf_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='从PDF文件中提取文本内容 (支持OCR识别扫描版PDF)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s document.pdf
  %(prog)s /path/to/file.pdf
  %(prog)s document.pdf -o output.txt
  %(prog)s document.pdf --ocr                    # OCR识别扫描版PDF
  %(prog)s document.pdf --pages 1-8              # 只提取第1-8页
  %(prog)s document.pdf --pages 3,4,5,6          # 只提取第3,4,5,6页
  %(prog)s document.pdf --pages 1-3,5,7-9 --ocr  # 组合使用
        """
    )

    parser.add_argument(
        'pdf_path',
        type=str,
        help='PDF文件路径'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出文件路径（可选，默认输出到终端）'
    )

    parser.add_argument(
        '-p', '--pages',
        type=str,
        help='指定要提取的页数，支持范围和逗号分隔，如: "1-8" 或 "3,4,5,6" 或 "1-3,5,7-9"'
    )

    parser.add_argument(
        '--no-layout',
        action='store_true',
        help='不保留文本布局'
    )

    parser.add_argument(
        '--ocr',
        action='store_true',
        help='使用OCR识别扫描版PDF（需要安装pytesseract和tesseract-ocr）'
    )

    args = parser.parse_args()

    # 验证文件是否存在
    pdf_file = Path(args.pdf_path)
    if not pdf_file.exists():
        print(f"错误: 文件不存在 '{args.pdf_path}'")
        sys.exit(1)

    if not pdf_file.suffix.lower() == '.pdf':
        print(f"警告: 文件可能不是PDF格式 (扩展名: {pdf_file.suffix})")

    # 提取文本
    preserve_layout = not args.no_layout
    text = extract_text_from_pdf(args.pdf_path, preserve_layout, use_ocr=args.ocr, page_range=args.pages)

    # 输出结果
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\n文本已保存到: {args.output}")
        except Exception as e:
            print(f"错误: 无法写入文件 - {e}")
            sys.exit(1)
    else:
        print(text)
        print("\n" + "=" * 80)
        print("提取完成")


if __name__ == '__main__':
    main()
