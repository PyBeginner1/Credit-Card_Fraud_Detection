# Credit Card Fraud Detection

Deployment: http://fraud-creditcard-env.eba-jeymp2ib.us-east-1.elasticbeanstalk.com/


## Credit Card Fraud:
According to data from the Reserve Bank of India (RBI), over a period of 10 years between April 2009 and September 2019, fraudsters managed to extract ₹615.39 crore from more than 1.17 lakh cases of credit and debit card frauds. However, the actual amount could be much higher since the bank did not keep records of cybercrimes under ₹1 lakh between April 2009 and April 2017.

In a survey conducted by online marketplace OLX in February 2020, it was revealed that 52% of the 7,500 respondents publicly shared their phone numbers and personal addresses online, with 26% of them also sharing one-time passwords (OTP) with others, and 22% admitting to sharing bank account, UPI, credit or debit card PIN details.

The RBI data showed that between April 2009 and April 2017, 100-odd banks reported 6,785 cases of credit/debit card fraud, resulting in a loss of ₹243.95 crore. However, after the RBI started tracking frauds under ₹1 lakh from April 2017, there was a significant increase in the number of reported cases. Within just two-and-a-half years (between April 2017 and September 2019), a total of 1,10,367 cases amounting to ₹371.44 crore were reported.


## Machine learning for credit card fraud detection:
Credit card fraud detection (CCFD) is like looking for needles in a haystack. It requires finding, out of millions of daily transactions, which ones are fraudulent. Due to the ever-increasing amount of data, it is now almost impossible for a human specialist to detect meaningful patterns from transaction data. For this reason, the use of machine learning techniques is now widespread in the field of fraud detection, where information extraction from large datasets is required.

Machine learning (ML) is a powerful tool for detecting credit card fraud because it can quickly and accurately analyze large amounts of data and identify patterns that may be difficult for humans to discern. Credit card fraud is a significant problem for banks, credit card companies, and their customers, and ML can help reduce the risk and minimize losses.

ML algorithms can be trained on large datasets of credit card transactions to learn patterns and anomalies that are indicative of fraud. These patterns may include unusual purchasing behavior, unusual geographical locations, unusual transaction amounts, and more. By analyzing these patterns, ML algorithms can identify potentially fraudulent transactions and alert financial institutions to investigate further.

Moreover, ML can continually learn from new data and adapt to changing patterns of fraud, making it a useful tool for combating evolving types of credit card fraud.


## Transaction data simulator:

This section presents a transaction data simulator of legitimate and fraudulent transactions. This simulator will be used throughout the rest of this book to motivate and assess the efficiency of different fraud detection techniques in a reproducible way.

A simulation is necessarily an approximation of reality. Compared to the complexity of the dynamics underlying real-world payment card transaction data, the data simulator that we present below follows a simple design.

This simple design is a choice. First, having simple rules to generate transactions and fraudulent behaviors will help in interpreting the kind of patterns that different fraud detection techniques can identify. Second, while simple in its design, the data simulator will generate datasets that are challenging to deal with.

The simulated datasets will highlight most of the issues that practitioners of fraud detection face using real-world data. In particular, they will include class imbalance (less than 1% of fraudulent transactions), a mix of numerical and categorical features (with categorical features involving a very large number of values), non-trivial relationships between features, and time-dependent fraud scenarios.


## Design choices:
Transaction features
Our focus will be on the most essential features of a transaction. In essence, a payment card transaction consists of any amount paid to a merchant by a customer at a certain time. The six main features that summarise a transaction therefore are:

- The transaction ID: A unique identifier for the transaction
- The date and time: Date and time at which the transaction occurs
- The customer ID: The identifier for the customer. Each customer has a unique identifier
- The terminal ID: The identifier for the merchant (or more precisely the terminal). Each terminal has a unique identifier
- The transaction amount: The amount of the transaction.
- The fraud label: A binary variable, with the value 0 for a legitimate transaction, or the value 1 for a fraudulent transaction.
These features will be referred to as TRANSACTION_ID, TX_DATETIME, CUSTOMER_ID, TERMINAL_ID, TX_AMOUNT, and TX_FRAUD.

The goal of the transaction data simulator will be to generate a table of transactions with these features


## Transaction generation process:
The simulation will consist of five main steps:

1. Generation of customer profiles: Every customer is different in their spending habits. This will be simulated by defining some properties for each customer. The main properties will be their geographical location, their spending frequency, and their spending amounts. The customer properties will be represented as a table, referred to as the customer profile table.
2. Generation of terminal profiles: Terminal properties will simply consist of a geographical location. The terminal properties will be represented as a table, referred to as the terminal profile table.
3. Association of customer profiles to terminals: We will assume that customers only make transactions on terminals that are within a radius of 
 of their geographical locations. This makes the simple assumption that a customer only makes transactions on terminals that are geographically close to their location. This step will consist of adding a feature 'list_terminals' to each customer profile, that contains the set of terminals that a customer can use.
4. Generation of transactions: The simulator will loop over the set of customer profiles, and generate transactions according to their properties (spending frequencies and amounts, and available terminals). This will result in a table of transactions.
5. Generation of fraud scenarios: This last step will label the transactions as legitimate or genuine. This will be done by following three different fraud scenarios.


## Fraud scenarios generation:
This last step of the simulation adds fraudulent transactions to the dataset, using the following fraud scenarios:

Scenario 1: Any transaction whose amount is more than 220 is a fraud. This scenario is not inspired by a real-world scenario. Rather, it will provide an obvious fraud pattern that should be detected by any baseline fraud detector. This will be useful to validate the implementation of a fraud detection technique.

Scenario 2: Every day, a list of two terminals is drawn at random. All transactions on these terminals in the next 28 days will be marked as fraudulent. This scenario simulates a criminal use of a terminal, through phishing for example. Detecting this scenario will be possible by adding features that keep track of the number of fraudulent transactions on the terminal. Since the terminal is only compromised for 28 days, additional strategies that involve concept drift will need to be designed to efficiently deal with this scenario.

Scenario 3: Every day, a list of 3 customers is drawn at random. In the next 14 days, 1/3 of their transactions have their amounts multiplied by 5 and marked as fraudulent. This scenario simulates a card-not-present fraud where the credentials of a customer have been leaked. The customer continues to make transactions, and transactions of higher values are made by the fraudster who tries to maximize their gains. Detecting this scenario will require adding features that keep track of the spending habits of the customer. As for scenario 2, since the card is only temporarily compromised, additional strategies that involve concept drift should also be designed.


## Supervised learning:
![Alt text](https://fraud-detection-handbook.github.io/fraud-detection-handbook/_images/baseline_ML_workflow.png)


## Challenges:
- Class imbalance: Real-world transaction data is mostly composed of legitimate transactions, with fraudulent transactions accounting for less than 1% of the total. Working with imbalanced data can pose a challenge for machine learning algorithms, which may struggle to handle large differences between classes. Therefore, we use the Strattified Shuffle split technique, which helps balance the distribution and address this issue.

- Data Drift: Patterns of transactions and fraud can evolve over time, with changes occurring in both the spending habits of credit card users and the techniques used by fraudsters. Credit card users' spending habits may vary depending on factors such as weekdays, weekends, vacations, and changes in their overall behavior over time. Meanwhile, fraudsters may adapt their tactics as older ones become ineffective.

- Lack of datasets to train: Due to confidentiality concerns, real-world credit card transaction data cannot be made public.
