from flask import Flask, request
from database import db
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def payment_webhook():
    data = request.json
    telegram_id = data.get("telegram_id")
    payment_status = data.get("payment_status")

    if payment_status == "success":
        subscription_end = datetime.now() + timedelta(days=7)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET payment_status = TRUE, subscription_end = ? WHERE telegram_id = ?", 
                       (subscription_end, telegram_id))
        db.commit()

    return "OK", 200
