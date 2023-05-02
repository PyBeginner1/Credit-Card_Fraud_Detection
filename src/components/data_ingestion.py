import os, sys
import pandas as pd
import numpy as np
import random
import time
from sklearn.model_selection import StratifiedShuffleSplit

from src.logger import logging
from src.exception import FraudException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.constant import *

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def generate_customer_profiles_table(self,n_customers, random_state=0):
        try:
            logging.info('Generating Customer profiles table')
            np.random.seed(random_state)
                
            customer_id_properties=[]
            
            # Generate customer properties from random distributions 
            for customer_id in range(n_customers):
                
                x_customer_id = np.random.uniform(0,100)
                y_customer_id = np.random.uniform(0,100)
                
                mean_amount = np.random.uniform(5,100) # Arbitrary (but sensible) value 
                std_amount = mean_amount/2 # Arbitrary (but sensible) value
                
                mean_nb_tx_per_day = np.random.uniform(0,4) # Arbitrary (but sensible) value 
                
                customer_id_properties.append([customer_id,
                                            x_customer_id, y_customer_id,
                                            mean_amount, std_amount,
                                            mean_nb_tx_per_day])
                
            customer_profiles_table = pd.DataFrame(customer_id_properties, columns=['CUSTOMER_ID',
                                                                            'x_customer_id', 'y_customer_id',
                                                                            'mean_amount', 'std_amount',
                                                                            'mean_nb_tx_per_day'])
            
            return customer_profiles_table
        except Exception as e:
            raise FraudException(e, sys) from e

    def generate_terminal_profiles_table(self,n_terminals, random_state=0):
        try:
            logging.info('Generating Terminal profiles table')
            np.random.seed(random_state)
                
            terminal_id_properties=[]
            
            # Generate terminal properties from random distributions in Latitude and Longitude
            for terminal_id in range(n_terminals):
                
                x_terminal_id = np.random.uniform(0,100)
                y_terminal_id = np.random.uniform(0,100)
                
                terminal_id_properties.append([terminal_id,
                                            x_terminal_id, y_terminal_id])
                                            
            terminal_profiles_table = pd.DataFrame(terminal_id_properties, columns=['TERMINAL_ID',
                                                                            'x_terminal_id', 'y_terminal_id'])
            
            return terminal_profiles_table
        except Exception as e:
            raise FraudException(e, sys) from e
    

    def get_list_terminals_within_radius(self,customer_profile, x_y_terminals, r):
        try:
        # Use numpy arrays in the following to speed up computations
            
            # Location (x,y) of customer as numpy array
            x_y_customer = customer_profile[['x_customer_id','y_customer_id']].values.astype(float)
            
            # Squared difference in coordinates between customer and terminal locations
            squared_diff_x_y = np.square(x_y_customer - x_y_terminals)
            
            # Sum along rows and compute suared root to get distance
            dist_x_y = np.sqrt(np.sum(squared_diff_x_y, axis=1))
            
            # Get the indices of terminals which are at a distance less than r
            available_terminals = list(np.where(dist_x_y<r)[0])
            
            # Return the list of terminal IDs
            return available_terminals
        except Exception as e:
            raise FraudException(e, sys) from e
    

    def generate_transactions_table(self,customer_profile, start_date = "2018-04-01", nb_days = 10):
        try:
            customer_transactions = []
            
            random.seed(int(customer_profile.CUSTOMER_ID))
            np.random.seed(int(customer_profile.CUSTOMER_ID))
            
            # For all days
            for day in range(nb_days):
                
                # Random number of transactions for that day 
                nb_tx = np.random.poisson(customer_profile.mean_nb_tx_per_day)
                
                # If nb_tx positive, let us generate transactions
                if nb_tx>0:
                    
                    for tx in range(nb_tx):
                        
                        # Time of transaction: Around noon, std 20000 seconds. This choice aims at simulating the fact that 
                        # most transactions occur during the day.
                        time_tx = int(np.random.normal(86400/2, 20000))
                        
                        # If transaction time between 0 and 86400, let us keep it, otherwise, let us discard it
                        if (time_tx>0) and (time_tx<86400):
                            
                            # Amount is drawn from a normal distribution  
                            amount = np.random.normal(customer_profile.mean_amount, customer_profile.std_amount)
                            
                            # If amount negative, draw from a uniform distribution
                            if amount<0:
                                amount = np.random.uniform(0,customer_profile.mean_amount*2)
                            
                            amount=np.round(amount,decimals=2)
                            
                            if len(customer_profile.available_terminals)>0:
                                
                                terminal_id = random.choice(customer_profile.available_terminals)
                            
                                customer_transactions.append([time_tx+day*86400, day,
                                                            customer_profile.CUSTOMER_ID, 
                                                            terminal_id, amount])
                    
            customer_transactions = pd.DataFrame(customer_transactions, columns=['TX_TIME_SECONDS', 'TX_TIME_DAYS', 'CUSTOMER_ID', 'TERMINAL_ID', 'TX_AMOUNT'])
            
            if len(customer_transactions)>0:
                customer_transactions['TX_DATETIME'] = pd.to_datetime(customer_transactions["TX_TIME_SECONDS"], unit='s', origin=start_date)
                customer_transactions=customer_transactions[['TX_DATETIME','CUSTOMER_ID', 'TERMINAL_ID', 'TX_AMOUNT','TX_TIME_SECONDS', 'TX_TIME_DAYS']]
            
            return customer_transactions  
        except Exception as e:
            raise FraudException(e, sys) from e
    

    def generate_dataset(self,n_customers = 10000, n_terminals = 1000000, nb_days=90, start_date="2018-04-01", r=5):
        try:
            logging.info('Generating Dataset')
            start_time=time.time()
            customer_profiles_table = self.generate_customer_profiles_table(n_customers, random_state = 0)
            logging.info("Time to generate customer profiles table: {0:.2}s".format(time.time()-start_time))
            
            start_time=time.time()
            terminal_profiles_table = self.generate_terminal_profiles_table(n_terminals, random_state = 1)
            logging.info("Time to generate terminal profiles table: {0:.2}s".format(time.time()-start_time))
            
            start_time=time.time()
            x_y_terminals = terminal_profiles_table[['x_terminal_id','y_terminal_id']].values.astype(float)
            customer_profiles_table['available_terminals'] = customer_profiles_table.apply(lambda x : self.get_list_terminals_within_radius(x, x_y_terminals=x_y_terminals, r=r), axis=1)
            # With Pandarallel
            #customer_profiles_table['available_terminals'] = customer_profiles_table.parallel_apply(lambda x : get_list_closest_terminals(x, x_y_terminals=x_y_terminals, r=r), axis=1)
            customer_profiles_table['nb_terminals']=customer_profiles_table.available_terminals.apply(len)
            logging.info("Time to associate terminals to customers: {0:.2}s".format(time.time()-start_time))
            
            start_time=time.time()
            transactions_df=customer_profiles_table.groupby('CUSTOMER_ID').apply(lambda x : self.generate_transactions_table(x.iloc[0], nb_days=nb_days)).reset_index(drop=True)
            # With Pandarallel
            #transactions_df=customer_profiles_table.groupby('CUSTOMER_ID').parallel_apply(lambda x : generate_transactions_table(x.iloc[0], nb_days=nb_days)).reset_index(drop=True)
            logging.info("Time to generate transactions: {0:.2}s".format(time.time()-start_time))
            
            # Sort transactions chronologically
            transactions_df=transactions_df.sort_values('TX_DATETIME')
            # Reset indices, starting from 0
            transactions_df.reset_index(inplace=True,drop=True)
            transactions_df.reset_index(inplace=True)
            # TRANSACTION_ID are the dataframe indices, starting from 0
            transactions_df.rename(columns = {'index':'TRANSACTION_ID'}, inplace = True)
            
            return (customer_profiles_table, terminal_profiles_table, transactions_df)
        except Exception as e:
            raise FraudException(e, sys) from e


    def add_frauds(self, customer_profiles_table, terminal_profiles_table, transactions_df):
    
        # By default, all transactions are genuine
        transactions_df['TX_FRAUD']=0
        transactions_df['TX_FRAUD_SCENARIO']=0
        
        # Scenario 1
        transactions_df.loc[transactions_df.TX_AMOUNT>220, 'TX_FRAUD']=1
        nb_frauds_scenario_1=transactions_df.TX_FRAUD.sum()
        logging.info("Number of frauds from scenario 1: "+str(nb_frauds_scenario_1))
        
        # Scenario 2
        for day in range(transactions_df.TX_TIME_DAYS.max()):
            
            compromised_terminals = terminal_profiles_table.TERMINAL_ID.sample(n=2, random_state=day)
            
            compromised_transactions=transactions_df[(transactions_df.TX_TIME_DAYS>=day) & 
                                                        (transactions_df.TX_TIME_DAYS<day+28) & 
                                                        (transactions_df.TERMINAL_ID.isin(compromised_terminals))]
                                
            transactions_df.loc[compromised_transactions.index,'TX_FRAUD']=1
        
        nb_frauds_scenario_2=transactions_df.TX_FRAUD.sum()-nb_frauds_scenario_1
        logging.info("Number of frauds from scenario 2: "+str(nb_frauds_scenario_2))
        
        # Scenario 3
        for day in range(transactions_df.TX_TIME_DAYS.max()):
            
            compromised_customers = customer_profiles_table.CUSTOMER_ID.sample(n=3, random_state=day).values
            
            compromised_transactions=transactions_df[(transactions_df.TX_TIME_DAYS>=day) & 
                                                        (transactions_df.TX_TIME_DAYS<day+14) & 
                                                        (transactions_df.CUSTOMER_ID.isin(compromised_customers))]
            
            nb_compromised_transactions=len(compromised_transactions)
            
            
            random.seed(day)
            index_fauds = random.sample(list(compromised_transactions.index.values),k=int(nb_compromised_transactions/3))
            
            transactions_df.loc[index_fauds,'TX_AMOUNT']=transactions_df.loc[index_fauds,'TX_AMOUNT']*5
            transactions_df.loc[index_fauds,'TX_FRAUD']=1
            
                                
        nb_frauds_scenario_3=transactions_df.TX_FRAUD.sum()-nb_frauds_scenario_2-nb_frauds_scenario_1
        logging.info("Number of frauds from scenario 3: "+str(nb_frauds_scenario_3))
        
        return transactions_df    
        
    
    def split_data_into_train_test(self, data):
        try:
            filename = FILE_NAME
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, filename)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, filename)

            logging.info('Splitting data into train and test')

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=1)

            train_df = None
            test_df = None

            for train_idx, test_idx in split.split(data, data['TX_FRAUD']):
                train_df = data.loc[train_idx]
                test_df = data.loc[test_idx]

            if train_df is not None:
                os.makedirs(os.path.dirname(train_file_path), exist_ok = True)
                logging.info(f"Exporting train dataset to filepath: [{train_file_path}]")
                train_df.to_csv(train_file_path)

            if test_df is not None:
                os.makedirs(os.path.dirname(test_file_path), exist_ok = True)
                logging.info(f"Exporting test dataset to filepath: [{test_file_path}]")
                test_df.to_csv(test_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                                        train_file_path=train_file_path,
                                        test_file_path=test_file_path,
                                        is_ingested = True,
                                        message = 'Data Ingestion successfull'
                                        )

            logging.info(f"Data Ingestion Artifact: [{data_ingestion_artifact}]")   
            return data_ingestion_artifact
        except Exception as e:
            raise FraudException(e, sys) from e 
    

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            (customer_profiles_table, terminal_profiles_table, transactions_df)=self.generate_dataset(n_customers = 5000, 
                                                        n_terminals = 10000, 
                                                        nb_days=183, 
                                                        start_date="2018-04-01", 
                                                        r=5)

            transactions_df = self.add_frauds(customer_profiles_table,terminal_profiles_table,transactions_df)

            data_ingestion_artifact = self.split_data_into_train_test(transactions_df)
            
            return data_ingestion_artifact
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
