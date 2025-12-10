# FastAPI OCR Project

### 1\. Environment Setup

Create a `.env` file in the root directory. It must contain the variables defined in `app/core/config.py`.

**Example `.env`:**

```ini
DATABASE_URL=postgresql://user:password@localhost:5432/ocr_db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 2\. Running the Application

**Start the API Server:**

```bash
uv run uvicorn app.main:app --reload
```

**Start the Celery Worker:**

```bash
uv run celery -A app.core.celery_config worker --loglevel=info
```

*(Note: Run the worker in a separate terminal window.)*
