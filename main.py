from customer_segmentation import Clusters, CustomerData, Elbow, NormalizedData, raw_data
from high_risk_countries import HighRiskCountry
from high_risk_customers import HighRiskCustomers, HighRiskScore
from plots import ClusterPlots, CountryPlots, ElbowPlot

print_now = "yes"

data = raw_data('Files/Data for assignment.xlsx')
print(data.info)
print(data.describe)

# Clean and prepare
data.impute()
data.dropnan()
X_encoded = data.dummies()

# Group the transactions by customer ID and aggregate
customer_summary = CustomerData(X_encoded).rename_columns()

# Normalize
X_norm = NormalizedData(customer_summary).normalize()

# Find numbers of clusters from elbowplot
k_range, inertia = Elbow().elbow(X_norm)
ElbowPlot(X_norm, print_=print_now).elbow_plot(k_range, inertia)

# Input number of clusters from the plot
number_of_clusters = 5

# Cluster the data, and add to summary
clusters = Clusters(5, X_norm).add_clusters(customer_summary)

# Add total transaction count
customer_summary['Count Trans'] = customer_summary['Credit Count']\
                                + customer_summary['Debit Count']

# Show plots of clusters
cust_plots = ClusterPlots(customer_summary, print_=print_now).show_all_plots()

# Find high-risk customers score
high_risk = HighRiskScore(customer_summary[customer_summary.columns[:9]], X_norm)
risk_score = high_risk.risk_score()
customer_summary['Risk Score'] = risk_score

# Find high risk customers
high_risk_cust = HighRiskCustomers(customer_summary)
high_risk_id = high_risk_cust.find_high_risk_customers(clusters)

# Add a separate cluster for high_risk customers
high_risk_cust_data = high_risk_cust.create_new_cluster(high_risk_id)

# Show data
susp_cust = high_risk_cust_data[high_risk_cust_data['cluster'] == 5]
susp_cust = susp_cust.loc[:,['Total Amount', 'Mean Amount',\
                            'Max Amount', 'Num Countries',\
                            'Credit Count', 'Debit Count']]

print(susp_cust)
print(susp_cust.describe())

# Show plots of high_risk_customers
highrisk_plots = ClusterPlots(high_risk_cust_data, print_=print_now).show_all_plots()


# Find trans to high_risk countries
risk_countries = HighRiskCountry(X_encoded)
data_agg = risk_countries.aggregate()
treshold = data_agg.quantile(0.75)[0]
customer_ids = risk_countries.find_customer_id(treshold)

#Plot high risk
CountryPlots(data_agg, print_=print_now).split_data()

# Describe
risk_countries.find_data(customer_summary, customer_ids)