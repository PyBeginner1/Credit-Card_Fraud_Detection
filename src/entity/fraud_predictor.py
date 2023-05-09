import os,sys
import pandas as pd
from datetime import datetime

from src.exception import FraudException
from src.util.util import load_object




class FraudData:
    def __init__(self, txn_day,txn_month,transaction_id, customer_id,terminal_id,txn_amt,txn_seconds,txn_days):
        try:
            self.txn_day = txn_day
            self.txn_month = txn_month
            self.transaction_id = transaction_id
            self.customer_id = customer_id
            self.terminal_id = terminal_id
            self.txn_amt = txn_amt
            self.txn_seconds = txn_seconds
            self.txn_days = txn_days
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def get_fraud_dataframe(self):
        try:
            fraud_input_dict = self.get_fraud_data_as_dict()
            return pd.DataFrame(fraud_input_dict)
        except Exception as e:
            raise FraudException(e, sys) from e


    def get_fraud_data_as_dict(self):
        try:
            input_data = {
            "TRANSACTION_ID" : [self.transaction_id],
            "CUSTOMER_ID": [self.customer_id],
            "TERMINAL_ID": [self.terminal_id],
            "TX_AMOUNT" : [self.txn_amt],
            "TX_TIME_SECONDS" : [self.txn_seconds],
            "TX_TIME_DAYS" : [self.txn_days],
            "day": [self.txn_day],
            "month": [self.txn_month],
            }
            return input_data
        except Exception as e:
            raise FraudException(e, sys) from e
        


class DataValidator:
    def __init__(self, dataframe):
        try:
            self.dataframe = dataframe
            self.txn_day = int(self.dataframe['day'].iloc[0])
            self.txn_month = int(self.dataframe['month'].iloc[0])
            self.transaction_id = int(self.dataframe['TRANSACTION_ID'].iloc[0])
            self.customer_id = int(self.dataframe['CUSTOMER_ID'].iloc[0])
            self.terminal_id = int(self.dataframe['TERMINAL_ID'].iloc[0])
            self.txn_amt = float(self.dataframe['TX_AMOUNT'].iloc[0])
            self.txn_seconds = int(self.dataframe['TX_TIME_SECONDS'].iloc[0])
            self.txn_days = int(self.dataframe['TX_TIME_DAYS'].iloc[0])
        except Exception as e:
            raise FraudException(e, sys) from e
        
    
    def validate_feature_values(self):
        try:
            validator = True
            error_data = []
            if self.txn_day > 31:
                validator = False
                error_data.append('Transaction day')
            if self.txn_month in [4,6,9,11]:
                if self.txn_day > 30:
                    validator = False
                    error_data.append('Transaction day')
            elif self.txn_month == 2:
                if self.txn_day > 28:
                    validator = False
                    error_data.append('Transaction day')
            if self.txn_month > 12:
                validator = False
                error_data.append('Transaction Month')
            if self.customer_id > 4999:
                validator = False
                error_data.append("Customer ID")
            if self.terminal_id > 9999:
                validator = False
                error_data.append('Terminal ID')
            #if self.txn_amt > 2375:
            #    validator = False
            #    error_data.append('Transaction Amount')
            if 30 < self.txn_seconds > 15811197:
                validator = False
                error_data.append('Transaction Seconds')
            if self.txn_days > 182:
                validator = False
                error_data.append('Transaction days')
            return validator, error_data
        except Exception as e:
            raise FraudException(e, sys) from e


class FraudPredictor:
    def __init__(self, model_dir):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def get_latest_model_path(self):
        try:
            model_directories = [i.replace('-','').replace('_','') for i in os.listdir(self.model_dir)]
            latest_model_directory_uncleaned = max(model_directories)

            dt_obj = datetime.strptime(latest_model_directory_uncleaned, '%Y%m%d%H%M%S')
            latest_model_directory = dt_obj.strftime('%Y-%m-%d_%H-%M-%S')
            dir_path = os.path.join(self.model_dir, latest_model_directory)
            file_name = os.listdir(dir_path)[0]

            latest_model_path = os.path.join(dir_path, file_name)
            return latest_model_path
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path = model_path)
            fraud = model.predict(X)
            return fraud
        except Exception as e:
            raise FraudException(e, sys) from e
