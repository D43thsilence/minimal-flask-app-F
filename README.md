# Exhibition Generator

A small Flask app that uses the OpenAI API to generate an exhibition tombstone label, a curatorial description, and a museum-display image from one object prompt.

## Entry point

The application entry point is [`app.py`](app.py). It exposes the Flask application as `app` and defines these routes:

- `GET /` — displays the prompt form.
- `POST /` — sends the submitted prompt to the OpenAI API and renders the generated label, description, and image.
- `GET /image` — serves `output.png` if that file is present.

The HTML interface is in [`templates/index.html`](templates/index.html). Flask renders it automatically from the `templates` directory.

## Requirements

- Python 3.10 or newer is recommended.
- An OpenAI API key with access to the models configured in `app.py`.
- Network access while the app is generating content.

The app reads `OPENAI_API_KEY` from a `.env` file using `python-dotenv`. Keep this file private; it is already excluded by `.gitignore`.

## Setup and run

Run these commands from the project directory.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask openai python-dotenv gunicorn
```

Create `.env` in the project root and add your key:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Start the development server:

```bash
python app.py
```

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install flask openai python-dotenv gunicorn
```

Create `.env` in the project root and add your key:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Start the development server:

```powershell
python app.py
```

If `python` is not available on Windows, replace it with `py`. If PowerShell blocks activation, run this for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Use the app

After the server starts, open <http://127.0.0.1:5000> in a browser. Enter a description of an object and select **Generate Exhibition**.

Stop the development server with `Ctrl+C`. To leave the virtual environment, run:

```bash
deactivate
```

## Troubleshooting

- `OPENAI_API_KEY` errors: confirm that `.env` is in the same directory as `app.py`, is named exactly `.env`, and contains a valid key.
- `ModuleNotFoundError`: activate `venv` and reinstall the packages with `python -m pip install flask openai python-dotenv gunicorn`.
- The page does not load: confirm that `python app.py` is still running and browse to `http://127.0.0.1:5000`.
- Generation is slow or fails: the app makes three OpenAI API requests for each submission, so check the terminal output, API access, quota, and network connection.

## Production deployment

For a platform such as Render:

- Build command: `python -m pip install flask openai python-dotenv gunicorn`
- Start command: `gunicorn app:app --timeout 240`
- Environment variable: `OPENAI_API_KEY` set to your API key

Do not commit `.env` or expose your API key in source control. The Flask development server is intended for local development; use Gunicorn or the hosting platform's production server for deployment.
