import pandas as pd
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from Excel file
data = pd.read_excel('Data for assignment.xlsx')

data.info()
data.describe()

# Looking at the NaN for product (describe), the percentage is low,
# the missing values are randomly distributed and there is no
# apparant pattern to their occurrence.
# I will therefore impute the missing values to not lose data

# Impute missing values with mode
data['product_type'].replace(" ", data['product_type'].mode()[0], inplace=True)

#remove NaN from amount
# Dropping amount since this is a key value
# - if the trans has no value, was it even a trans done?
# Also dropping NaN from country - only 7 rows
data.dropna(inplace=True)

# perform one-hot encoding on categorical variables.
# I will leave country as it is, and only use the count
# of unique countries
X_encoded = pd.get_dummies(data, columns=['credit_debit',
                                          'product_type'])

# Group the transactions by customer ID and aggregate
customer_summary = X_encoded.groupby('customer_id').agg(
    {'amount': ['sum', 'mean', 'max'],
     'CPCC': pd.Series.nunique, 'credit_debit_Credit': "sum", 
     'credit_debit_Debit': 'sum', 'product_type_A1': "sum",
     'product_type_A2': 'sum', 'product_type_A3': 'sum'})

# Rename columns
customer_summary.columns = ['Total Amount', 'Mean amount',
        'Max amount', 'Num Countries',
        'Credit count', 'Debit count',
        'P1 count', 'P2 count', "P3 count"] 


# Normalize numerical features
scaler = StandardScaler()
X_norm = scaler.fit_transform(customer_summary)

# Use an elbow graph to find the optimal amount of clusters
# Define the range of the number of clusters to test
k_range = range(1, 20)

# Run KMeans for each k in the range and store the inertia in a list
inertia = []
for k in k_range:
    kmeans = KMeans(n_clusters=k,n_init=10, random_state=0).fit(X_norm)
    inertia.append(kmeans.inertia_)

# Plot the elbow curve to determine the optimal number of clusters
sns.set(style='whitegrid')
plt.plot(k_range, inertia)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Curve')
plt.show()

# Set number of clusters to 5 from the elbow graph
num_clusters = 5

# Perform clustering with current amount of clusters
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X_norm)
labels = kmeans.labels_

# Add cluster labels to customer summary data
customer_summary['cluster'] = labels

# View distribution of clusters
print(customer_summary.groupby('cluster').size())

# Get high_risk customers from group 3
# With number of countries above 10 
# and highest amount amongst this subset
customer_summary.loc[(customer_summary['cluster']==3) & \
                     (customer_summary['Num Countries'] > 10)]\
                     .sort_values(by="Total Amount", ascending=False)
