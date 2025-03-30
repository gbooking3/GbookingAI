# app_test.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(debug=True, port=port)
