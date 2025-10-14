<<<<<<< HEAD
# ID_OCR
=======
# Arabic ID Reader

A web-based Arabic OCR system scaffold. The goal is to detect, read, and extract text data from Arabic ID cards and display results via a web interface.

## Project Structure

```
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── upload_routes.py
│   │   └── ocr_routes.py
│   ├── services/
│   │   ├── detection_service.py
│   │   ├── recognition_service.py
│   │   └── storage_service.py
│   ├── models/
│   │   └── model_handler.py
│   └── utils/
│       └── helpers.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   └── extracted/
├── notebooks/
│   └── exploration.ipynb
├── docs/
│   └── project_report.md
├── main_pipeline.py
├── README.md
└── .gitignore
```

## Folder-by-Folder Overview

- **backend/**: API server (FastAPI or Flask). Hosts upload and OCR endpoints and orchestrates services.
  - **app.py**: App entry point. Initializes the framework and registers routes.
  - **requirements.txt**: Backend Python dependencies.
  - **routes/**: API route handlers.
    - **upload_routes.py**: Image upload and validation endpoints.
    - **ocr_routes.py**: Triggers detection and recognition; returns extracted data.
  - **services/**: Core business logic.
    - **detection_service.py**: Detects/crops regions (name, ID number, DOB) from ID images.
    - **recognition_service.py**: OCR over cropped regions (e.g., Hugging Face, PaddleOCR).
    - **storage_service.py**: Persists results to CSV/JSON under `data/extracted`.
  - **models/**:
    - **model_handler.py**: Loads/switches OCR models and runs inference.
  - **utils/**:
    - **helpers.py**: Shared utilities (validation, formatting).

- **frontend/**: Web UI for uploads and results display.
  - **index.html**: Upload form and results section.
  - **styles.css**: Minimal styling.
  - **script.js**: Handles user interactions and calls backend APIs.
  - **assets/**: Logos/images/icons used by the web UI.

- **data/**: Project datasets and outputs.
  - **raw/**: Original uploaded ID images.
  - **processed/**: Cropped/cleaned image regions.
  - **extracted/**: Final OCR outputs (CSV/JSON).

- **notebooks/**:
  - **exploration.ipynb**: Experiments with OCR models (Hugging Face, PaddleOCR).

- **docs/**:
  - **project_report.md**: Documentation and progress notes.

- **main_pipeline.py**: End-to-end pipeline script that ties together detection → recognition → storage; can be invoked offline for batch processing.

- **.gitignore**: Ignores environment files, caches, node_modules, and large data artifacts.

## Key Files Explained

- **backend/app.py**: Bootstraps the API application and mounts routes from `routes/`.
- **backend/routes/upload_routes.py**: Defines POST endpoint for image uploads.
- **backend/routes/ocr_routes.py**: Defines endpoints to run OCR on a given upload and return structured results.
- **backend/services/detection_service.py**: Performs object/region detection and cropping pipeline.
- **backend/services/recognition_service.py**: Wraps OCR models and post-processing for Arabic text.
- **backend/services/storage_service.py**: Serializes and stores OCR outputs.
- **backend/models/model_handler.py**: Abstraction for loading/switching OCR backends.
- **backend/utils/helpers.py**: Input validation, formatting, and common helpers.
- **frontend/index.html**: Basic UI layout and containers for upload/results.
- **frontend/script.js**: Fetch calls to backend upload/OCR endpoints and DOM updates.
- **main_pipeline.py**: CLI entry for batch processing.

## Data Flow

1. User uploads an image via the web UI (`frontend/index.html`).
2. Frontend sends the image to the backend upload endpoint (`routes/upload_routes.py`).
3. Backend stores the raw image under `data/raw/`.
4. Detection service (`services/detection_service.py`) locates key fields and writes crops to `data/processed/`.
5. Recognition service (`services/recognition_service.py`) runs OCR on crops and returns Arabic text with metadata.
6. Storage service (`services/storage_service.py`) writes structured outputs to `data/extracted/` as CSV/JSON.
7. Frontend polls/requests results and renders them in the browser (`frontend/script.js`).

## Data Flow Diagram (Markdown)

```
[User Browser]
     |
     v
[Frontend (index.html/script.js)] -- upload --> [Backend Upload Routes]
     |                                             |
     |                                             v
     |                                      [data/raw/]
     |                                             |
     |                                             v
     |                                   [Detection Service]
     |                                             |
     |                                             v
     |                                      [data/processed/]
     |                                             |
     |                                             v
     |                                   [Recognition Service]
     |                                             |
     |                                             v
     |                                   [Storage Service]
     |                                             |
     |                                             v
     |                                      [data/extracted/]
     |                                             |
     \------------------- results JSON <-----------/
```

## Getting Started (Scaffold)

1. Create a virtual environment and install backend deps:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r backend/requirements.txt
   ```
2. Choose a framework (FastAPI recommended) and initialize `backend/app.py`.
3. Implement routes/services incrementally following this structure.

## Deployment Notes

- Designed to separate backend API and frontend assets for easy containerization.
- Data directories are organized for persistence and auditing.
- Future steps can add Dockerfiles, CI, and hosting configs.


>>>>>>> 0461a4a (Arabic ID Reader project structure)
