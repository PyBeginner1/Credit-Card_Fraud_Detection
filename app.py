from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    try:
        if request.method == 'GET':
            return render_template('index.html')
        else:
            txn_day = request.form.get('day')
            txn_month = request.form.get('month')
            customer_id = request.form.get('customer-id')
            terminal_id = request.form.get('terminal-id')
            txn_amt = request.form.get('amount')
            txn_seconds = request.form.get('seconds')
            txn_days = request.form.get('days')
            print(txn_day,txn_month,customer_id,terminal_id,txn_amt,txn_seconds,txn_days)
    except Exception as e:
        raise e


if __name__ == '__main__':
    app.run(debug = True)