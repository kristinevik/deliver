import pandas as pd

# Load data from Excel file
data = pd.read_excel('Data for assignment.xlsx')

# Insert high_risk countries
high_risk_countries = pd.read_csv('high_risk_copy.csv')
high_risk = data.loc[(data['CPCC'].isin(\
                    high_risk_countries["Country_code"]))\
                    & (data['credit_debit']=='Debit')]

# Group the transactions by amount range
n = 2000
amount_bins = [0]
amount_labels = []
while n < 19000:
    label = f"{str(int((n/1000))-2)}k-{str(int(n/1000))}k"
    amount_labels.append(label)
    amount_bins.append(n)
    n += 2000

high_risk['Amount Range'] = pd.cut(high_risk['amount'], bins=amount_bins, labels=amount_labels)

# Create a bar chart of the transaction amounts by amount range
amount_counts = high_risk['Amount Range'].value_counts().sort_index()
amount_counts.plot(kind='bar')
plt.title('Distribution of Monthly Incoming Transaction Amounts from High-Risk Countries')
plt.xlabel('Amount Range')
plt.ylabel('Number of Transactions')
plt.savefig('45464.png')

#Find treshold
high_risk.groupby('customer_id').agg(
    {'amount': 'sum'}).describe() #6907 is at 75 % percentile. I will use this number


# Recommend an amount threshold for identifying potential unusual behavior
threshold_amount = 6907 # replace with your actual recommended threshold

# Identify customer IDs who would trigger the new rule
suspicious_customers = high_risk[high_risk['amount'] >= threshold_amount]['customer_id'].unique()
