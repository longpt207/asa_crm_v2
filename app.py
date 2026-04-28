from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # load file .env

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM customers;")
        customers_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM students;")
        students_count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "status": "ok",
            "customers": customers_count,
            "students": students_count
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)