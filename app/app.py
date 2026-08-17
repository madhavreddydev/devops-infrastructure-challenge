from flask import Flask
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppassword"),
        connect_timeout=3
    )


@app.route("/")
def home():
    return "Hello from Kubernetes!"


@app.route("/health")
def health():
    return "healthy", 200


@app.route("/ready")
def ready():
    try:
        connection = get_db_connection()
        connection.close()
        return "ready", 200
    except Exception as error:
        return f"database unavailable: {error}", 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
