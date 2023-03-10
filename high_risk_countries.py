import pandas as pd


class HighRiskCountry:
    def __init__(self, cleaned_data):
        self.cust_data = cleaned_data
        self.high_risk_countries = pd.read_csv('Files/high_risk_copy.csv')


    def find_transactions(self):
        # Insert high_risk countries
        return self.cust_data.loc[(self.cust_data['CPCC'].isin(\
                            self.high_risk_countries["Country_code"]))\
                            & (self.cust_data['credit_debit_Debit']==1)]

    def aggregate(self):
        transactions = self.find_transactions()
        return transactions.groupby('customer_id').agg(
                            {'amount': 'sum'}).sort_values(by='amount')


    def find_customer_id(self, treshold):
        agg_customers = self.aggregate()
        # Identify customer IDs who would trigger the new rule
        return agg_customers[agg_customers['amount'] >= treshold].index.unique()

    def find_data(self, customer_summary, customer_id):
        data = customer_summary[customer_summary.index.isin(customer_id)]
        # Describe the data
        print(data.describe())
        # Info
        print(data.info())