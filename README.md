# DocxDataApp

A web application for extracting named entities from DOCX files and text inputs.

---

## 🚀 Features

* **Entity Extraction from DOCX Files**: Upload DOCX files to extract named entities.
* **Entity Extraction from Text Input**: Paste or type text to extract named entities.

---


## ⚙️ Technologies

* **Backend**: FastAPI, spaCy
* **Frontend**: Streamlit
* **Deployment**: Render.com
* **Others**: python-docx, requests, python-multipart

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SID-9/DocxDataApp.git
cd DocxDataApp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend

```bash
uvicorn backend.main:app --reload
```

### 4. Run the Frontend

```bash
streamlit run frontend.app.py
```

---

## 🌐 Deployment

* **Backend**: [https://chatdataapp.onrender.com]
* **Frontend**: [https://chatdataapp-1.onrender.com](https://docxdataapp-1.onrender.com/)

