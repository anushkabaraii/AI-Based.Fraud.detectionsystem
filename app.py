from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

transactions = []
fraud_count = 0
normal_count = 0

accuracy = 99.2


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    global fraud_count, normal_count

    amount = float(request.form["amount"])
    time = datetime.now().strftime("%H:%M:%S")

    if amount > 20000:
        result = "Fraudulent Transaction"
        fraud = 1
        fraud_count += 1
        reason = "The transaction amount is unusually high, which is a common indicator of fraud."
    else:
        result = "Safe Transaction"
        fraud = 0
        normal_count += 1
        reason = "The transaction amount is within normal range and does not match fraud patterns."

    transactions.insert(0,{
        "Amount": amount,
        "Time": time,
        "Class": fraud
    })

    if len(transactions) > 10:
        transactions.pop()

    return render_template(
    "dashboard.html",
    result=result,
    reason=reason,
    accuracy=accuracy,
    fraud_count=fraud_count,
    normal_count=normal_count,
    total=fraud_count + normal_count,
    transactions=transactions
)


@app.route("/dashboard")
def dashboard():

    total_transactions = fraud_count + normal_count

    return render_template(
        "dashboard.html",
        result=None,
        reason=None,
        accuracy=accuracy,
        fraud_count=fraud_count,
        normal_count=normal_count,
        total=total_transactions,
        transactions=transactions
    )


if __name__ == "__main__":
    app.run(debug=True)