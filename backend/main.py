from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from .service import extract_entities_from_lines, extract_text_from_docx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/extract-entities")
async def extract_entities_from_docx(file: UploadFile = File(...)):
    tmp_path = None
    try:
        # Validate file type
        if not file.filename.endswith(".docx"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .docx files are allowed."
            )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Process the DOCX file
        lines = extract_text_from_docx(tmp_path)
        entities = extract_entities_from_lines(lines)

        return {"lines": lines, "entities": entities}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Always clean up temp file if it was created
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
