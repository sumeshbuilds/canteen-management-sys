"""Entry point for the College Canteen Management System.

Development:
    python app.py            # http://127.0.0.1:5000
    flask --app app run --debug

Production (see DOCUMENTATION.md):
    waitress-serve --listen=0.0.0.0:8000 app:app
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
