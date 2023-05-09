import os, sys
from flask import Flask, render_template, request

from src.entity.fraud_predictor import FraudData, DataValidator, FraudPredictor


ROOT_DIR = os.getcwd()
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)

FRAUD_DATA_KEY = "fraud_data"
FRAUD_VALUE_KEY = "fraud_value"

application = Flask(__name__)
app = application

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
            transaction_id = request.form.get('id')
            customer_id = request.form.get('customer-id')
            terminal_id = request.form.get('terminal-id')
            txn_amt = request.form.get('amount')
            txn_seconds = request.form.get('seconds')
            txn_days = request.form.get('days')

            fraud_dataframe = FraudData(txn_day = txn_day,
                                         txn_month = txn_month,
                                         transaction_id = transaction_id,
                                         customer_id = customer_id,
                                         terminal_id = terminal_id,
                                         txn_amt = txn_amt,
                                         txn_seconds = txn_seconds,
                                         txn_days = txn_days)
            fraud_df = fraud_dataframe.get_fraud_dataframe()
            #print(fraud_dataframe.get_fraud_data_as_dict())

            #Validating Input data
            data_validator = DataValidator(dataframe = fraud_df)   
            validator, error_feature_list = data_validator.validate_feature_values()   

            if validator == False:
                message = "The following fields are incorrect: "
                for feature in error_feature_list:
                    message += feature +', '
                message = message.rstrip(', ')
                return render_template('error.html', message=message)
            
            #Prediction
            predictor = FraudPredictor(model_dir=MODEL_DIR)
            result = predictor.predict(X=fraud_df)
            if result[0] == 0:
                result = 'The provided information is legitimate and not fraudulent'
            else:
                result = 'The provided information is Fraudulent'
            return render_template('predict.html', result = result)
    except Exception as e:
        raise e


if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0")