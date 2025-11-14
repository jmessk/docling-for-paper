from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse
from docling.document_converter import DocumentConverter
import tempfile
import os
import uvicorn


app = FastAPI(title="Docling PDF Converter")

# Create a single converter instance to reuse across requests
converter = DocumentConverter()

# Path to the served index.html
BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "index.html")


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(INDEX_PATH, media_type="text/html; charset=utf-8")


@app.post("/convert")
async def convert(file: UploadFile = File(...), format: str = Form(...)):
    # Basic validation
    ext_ok = (file.filename or "").lower().endswith(".pdf")
    type_ok = (file.content_type or "").lower() in {
        "application/pdf",
        "application/x-pdf",
        "application/acrobat",
    }
    if not (ext_ok or type_ok):
        raise HTTPException(
            status_code=400, detail="PDFファイルをアップロードしてください"
        )

    if format not in {"html", "markdown"}:
        raise HTTPException(
            status_code=400,
            detail="format は 'html' または 'markdown' を指定してください",
        )

    # Persist upload to a temporary .pdf file because DocumentConverter expects a filename
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            data = await file.read()
            tmp.write(data)
            tmp_path = tmp.name

        # Convert with Docling
        dl_doc = converter.convert(tmp_path)

        if format == "html":
            output = dl_doc.document.export_to_html()
            media_type = "text/html; charset=utf-8"
        else:
            output = dl_doc.document.export_to_markdown()
            media_type = "text/plain; charset=utf-8"

        return Response(content=output, media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"変換に失敗しました: {e}")
    finally:
        # Clean up temporary file
        try:
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def main():
    # Start the development server
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
