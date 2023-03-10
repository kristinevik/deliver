import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class raw_data:
    
    def __init__(self, filename):
        self.data = pd.read_excel(filename)
        self.info = self.data.info()
        self.describe = self.data.describe()


    def impute(self):
        # Looking at the NaN for product (describe), the percentage is low,
        # the missing values are randomly distributed and there is no
        # apparant pattern to their occurrence.
        # I will therefore impute the missing values to not lose data

        # Impute missing values with mode
        self.data['product_type'].replace(" ", self.data['product_type'].mode()[0], inplace=True)

    def dropnan(self):
        #remove NaN from amount
        # Dropping amount since this is a key value
        # - if the trans has no value, was it even a trans done?
        # Also dropping NaN from country - only 7 rows
        self.data.dropna(inplace=True)

    def dummies(self):
        # perform one-hot encoding on categorical variables.
        # I will leave country as it is, and only use the count
        # of unique countries
        return pd.get_dummies(self.data, columns=['credit_debit',
                                                'product_type'])


class CustomerData:

    def __init__(self, dummy_data):
        self.X_encoded = dummy_data

    def customer_summary(self):
        # Group the transactions by customer ID and aggregate
        return self.X_encoded.groupby('customer_id').agg(
            {'amount': ['sum', 'mean', 'max'],
            'CPCC': pd.Series.nunique, 'credit_debit_Credit': "sum", 
            'credit_debit_Debit': 'sum', 'product_type_A1': "sum",
            'product_type_A2': 'sum', 'product_type_A3': 'sum'})

    def rename_columns(self):
        customer_summ = self.customer_summary()
        customer_summ.columns = ['Total Amount', 'Mean Amount',
            'Max Amount', 'Num Countries',
            'Credit Count', 'Debit Count',
            'P1 Count', 'P2 Count', "P3 Count"]
        return customer_summ
        


class NormalizedData:

    def __init__(self, customer_summary):
        self.customer_summary = customer_summary


    def normalize(self):
        return StandardScaler().fit_transform(self.customer_summary)


class Elbow:

    def elbow(self, X_norm):
        # Define the range of the number of clusters to test
        k_range = range(1, 20)

        # Run KMeans for each k in the range and store the inertia in a list
        inertia = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k,n_init=10, random_state=0).fit(X_norm)
            inertia.append(kmeans.inertia_)

        return k_range, inertia


class Clusters:

    def __init__(self, number_of_clusters, X_norm):
        self.number_of_clusters = number_of_clusters
        self.X_norm = X_norm

    def clusters(self):
        # Perform clustering with current amount of clusters
        kmeans = KMeans(n_clusters=self.number_of_clusters, n_init=10, )
        kmeans.fit(self.X_norm)
        return kmeans.labels_
    
    def add_clusters(self, customer_summary):
        customer_summary['cluster'] = self.clusters()
        return customer_summary.groupby('cluster').size()




    




