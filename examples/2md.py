import sys
import os
from docling.document_converter import DocumentConverter


def main():
    converter = DocumentConverter()

    input_filename = sys.argv[1]
    doc = converter.convert(input_filename)
    markdown_output = doc.document.export_to_markdown()

    output_filename = os.path.splitext(os.path.basename(input_filename))[0] + "."
    os.makedirs("./output/", exist_ok=True)

    with open(f"./output/{output_filename}", "w") as f:
        f.write(markdown_output)


if __name__ == "__main__":
    main()
