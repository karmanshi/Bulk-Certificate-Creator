# Bulk Certificate Creator

A Django-based application for generating bulk PDF certificates for multiple recipients. The project exposes both a browser dashboard and a REST API for creating certificate jobs, monitoring progress, and downloading generated files.

## Project setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment if one is not already present:

```powershell
cd "K:\Bulk_Certificate_Generator\Bulk-Certificate-Creator"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install the application dependencies:

```powershell
pip install django djangorestframework reportlab pillow
```

4. Apply the database migrations:

```powershell
python manage.py migrate
```

This creates the SQLite database at `db.sqlite3` and prepares the `GenerationJob` and `Recipient` tables used by the certificate workflow.

## How to run the application

Start the development server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

Then open the dashboard in a browser:

- http://127.0.0.1:8000/

The dashboard lets you add recipients, submit a certificate generation request, watch job status, and download individual PDFs.

## How to run tests

The project uses Django's default test runner:

```powershell
python manage.py test
```

At the moment the project has no custom Django tests defined, so the command will report `Ran 0 tests` while still validating that the app boots cleanly.

## How to submit a certificate generation request

### Via the web dashboard

Use the form on the homepage, add one or more recipient rows, and click `Generate Certificates`.

### Via the API

Send a POST request to:

```http
POST /api/jobs/
Content-Type: application/json
```

Example:

```powershell
curl -X POST http://127.0.0.1:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": [
      {"name": "Jane Doe", "email": "jane@example.com"},
      {"name": "John Smith", "email": "john@example.com"}
    ]
  }'
```

Successful response:

```json
{
  "job_id": 1,
  "status": "COMPLETED",
  "total_recipients": 2,
  "successful_count": 2,
  "failed_count": 0
}
```

The job is created immediately and the application processes each recipient in sequence. You can also query a job’s full details through:

```http
GET /api/jobs/<job_id>/
```

This returns the current status, counts, and the per-recipient results for the job.

## How to retrieve generated certificates

### List all generated certificates

```http
GET /api/certificates/
```

This returns each recipient record with a `certificate_url` when a PDF was created successfully.

### Download a single certificate

```http
GET /api/certificates/<recipient_id>/download/
```

Example:

```powershell
curl -L http://127.0.0.1:8000/api/certificates/1/download/ -o certificate_1.pdf
```

The generated files are stored under `media/certificates/` and the API serves them as downloadable PDF attachments.

## Important implementation/design decisions

- Django + Django REST Framework: the app is built as a standard Django project with DRF endpoints, which makes it easy to expose both an HTML dashboard and API-based workflows.
- SQLite for local development: the project uses `db.sqlite3` by default, which is sufficient for a lightweight bulk generation tool and makes local setup simple.
- Job/Recipient model split: `GenerationJob` tracks overall status and totals, while each `Recipient` keeps its own result, generated file, and error message. This gives a clear per-recipient audit trail.
- File generation at the application layer: certificate PDFs are generated using `reportlab` and saved under `media/certificates/`. The `certificate` field on each recipient stores the final PDF file reference.
- Synchronous request processing by default: `GenerationJobCreateView` calls `process_generation_job(job)` directly after creating the database records. This keeps the system simple and predictable for local development; the background processor is available in the codebase but is not enabled by default.
- Dashboard-first UX: the root page uses JavaScript fetch calls to the API, making it easy to build and test the feature without a separate frontend app.
- Validation and status tracking: the serializer enforces at least one recipient and the processing flow updates each recipient status (`PENDING`, `PROCESSING`, `SUCCESS`, `FAILED`) while the job status moves through `PENDING`, `PROCESSING`, and terminal states such as `COMPLETED` or `COMPLETED_WITH_ERRORS`.

## Typical workflow

1. Start the app with `python manage.py runserver`.
2. Open the dashboard at `http://127.0.0.1:8000/`.
3. Add recipient names and email addresses.
4. Submit the certificate job via the browser or API.
5. Poll the `GET /api/jobs/<job_id>/` endpoint or watch the dashboard until the job completes.
6. Download PDFs from the certificate list or the individual recipient download endpoint.

## Notes

- Media files are served in debug mode via Django static media handling.
- For a production deployment, configure a real secret key, a secure database, and a production-grade static/media hosting strategy.
