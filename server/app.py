# app_test.py
from app import create_app
import os

app = create_app()


@app.route('/')
def hello():
    return "Hello from mobile Gbooking server!"

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5000)

    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(debug=True, port=port)
