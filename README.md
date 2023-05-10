# Credit Card Fraud Detection

Deployment: http://fraud-creditcard-env.eba-jeymp2ib.us-east-1.elasticbeanstalk.com/


## Credit Card Fraud:
According to data from the Reserve Bank of India (RBI), over a period of 10 years between April 2009 and September 2019, fraudsters managed to extract ₹615.39 crore from more than 1.17 lakh cases of credit and debit card frauds. However, the actual amount could be much higher since the bank did not keep records of cybercrimes under ₹1 lakh between April 2009 and April 2017.

In a survey conducted by online marketplace OLX in February 2020, it was revealed that 52% of the 7,500 respondents publicly shared their phone numbers and personal addresses online, with 26% of them also sharing one-time passwords (OTP) with others, and 22% admitting to sharing bank account, UPI, credit or debit card PIN details.

The RBI data showed that between April 2009 and April 2017, 100-odd banks reported 6,785 cases of credit/debit card fraud, resulting in a loss of ₹243.95 crore. However, after the RBI started tracking frauds under ₹1 lakh from April 2017, there was a significant increase in the number of reported cases. Within just two-and-a-half years (between April 2017 and September 2019), a total of 1,10,367 cases amounting to ₹371.44 crore were reported.


## Means of payment card fraud:
There are two types of card fraud, namely card-present fraud (less common these days) and card-not-present fraud (more common). The compromise can occur in various ways and often takes place without the cardholder's knowledge. The internet has made database security lapses particularly costly, and in some cases, millions of accounts have been compromised.

In situations where a card is stolen, the cardholder can quickly report it to the issuing bank, but if the account details have been compromised, fraudsters may hold onto them for months before any theft occurs, making it challenging to identify the source of the breach. The cardholder may only become aware of fraudulent activity after receiving a statement. To mitigate this risk, cardholders should frequently check their accounts to ensure there are no suspicious or unknown transactions.

When a credit card is lost or stolen, it can be used for illicit purchases until the holder informs the issuing bank, and the bank places a block on the account. Most banks offer free 24-hour telephone numbers to encourage prompt reporting. However, it is still possible for a thief to make unauthorized purchases on a card before it is cancelled.

## Card-Present Fraud:
Card-present fraud is a transaction in which the fraudulent party physically presents the counterfeit credit card to the merchant. A simple example of card-present fraud would be when a thief steals a credit card and then simply uses that card in-person at a store to make a purchase. Sometimes these incidents can be detected by the store staff; one example is when the buyer seems unusually eager to process the transaction quickly. Other tactics sometimes used by card-present fraudulent parties include trying to distract the merchant to prevent them from scrutinizing the card, or showing up very close to the opening or closing times of the store when there may be less staff present to handle anti-fraud procedures. 

Card-present fraud has become less common because credit card thieves have shifted their attention to online forms of credit card fraud. Online credit card theft allows hackers to access potentially far larger pools of credit card information without needing to expose themselves to the risk of in-person detection at a store. Moreover, with large merchants holding vast databases of credit card information, online cybercrime allows hackers to potentially access hundreds of thousands or even millions of credit cards at once.

## Card not present Fraud:
A card-not-present transaction (CNP, mail order / telephone order, MO/TO) is a payment card transaction made where the cardholder does not or cannot physically present the card for a merchant's visual examination at the time that an order is given and payment effected. It is most commonly used for payments made over the Internet, but can also be used with mail-order transactions by mail or fax, or over the telephone.

Card-not-present transactions are a major route for credit card fraud, because it is difficult for a merchant to verify that the actual cardholder is indeed authorizing a purchase.

Examples: 
- Online orders: A customer adds products to an online shopping cart and checks out using their card details.
- Buy online, pickup in-store (BOPIS): Similar to online orders, but the customer picks up their order instead of having it delivered.
- Phone orders: A customer makes an order over the phone, calling out their credit card details to the sales agent who then processes the payment.
- Mail orders: Payments sent by post; for example, when ordering from a physical product catalog.

![Alt text](https://www.insiderintelligence.com/content/storage/29c443c7620df8d6118b5ca811fd112e/277849)
Based on data from the US, card-not-present (CNP) fraud is expected to cause a loss of $9.49 billion this year, indicating an 8.5% increase over last year's figures. CNP fraud will account for 73.0% of all card payment fraud losses in 2021, which is a substantial increase from 57.0% in 2019.

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

## References:
- https://www.hindustantimes.com/cities/mumbai-news/thane-municipal-corporation-receives-over-90-complaints-about-water-pipeline-leakages-and-damages-since-january-101683660851807.html
- https://en.wikipedia.org/wiki/Credit_card_fraud
- https://www.investopedia.com/terms/c/cardpresent-fraud.asp#:~:text=What%20Is%20Card%2DPresent%20Fraud,card%20is%20not%20physically%20present.
- https://www.insiderintelligence.com/content/card-not-present-fraud-payment
