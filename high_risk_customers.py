from sklearn.preprocessing import StandardScaler

class HighRiskScore:

    def __init__(self, cust_data, normalized_data):
        self.cust_data = cust_data
        self.X_norm = normalized_data

    def risk_score(self):
        self.cust_data.loc[:,self.cust_data.columns] = self.X_norm
        return self.cust_data['Total Amount'] + self.cust_data['Num Countries']
        
       

class HighRiskCustomers:

    def __init__(self, customer_summary):
        self.customer_summary = customer_summary

    def separate_clusters(self, clusters):
        sorted_clusters = clusters.sort_values(ascending=False).index
        return sorted_clusters[:3], sorted_clusters[-2:]

    def find_high_risk_customers(self, clusters, amount = 11):
        big_clusters, small_clusters = self.separate_clusters(clusters)
        big_cluster_data = self.customer_summary[self.customer_summary['cluster'].isin(big_clusters)]
        cluster_high_risk =  self.customer_summary[self.customer_summary['cluster'].isin(small_clusters)].index
        customer_high_risk = big_cluster_data.sort_values(by='Risk Score', ascending=False).head(amount).index
        return cluster_high_risk.append(customer_high_risk)
    
    def create_new_cluster(self, high_risk):
        new_cluster = self.customer_summary
        new_cluster.loc[high_risk, 'cluster'] = 5
        return new_cluster