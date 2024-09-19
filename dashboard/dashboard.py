import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as mtick
import datetime as dt


# Load the data
all_df = pd.read_csv('main_data.csv')

# Define functions for processing data
def create_product_count_df(df):
    product_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_counts.sort_values(by='product_id', ascending=False)
    return sorted_df

def create_rating_service(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    max_score = rating_service.idxmax()
    return (rating_service, max_score)

def create_city_customer_df(df):
    city_customer = df.customer_city.value_counts().sort_values(ascending=False).rename_axis('City').reset_index(name='Number of Customers') 
    return city_customer

def create_city_seller_df(df):
    city_seller = df.seller_city.value_counts().sort_values(ascending=False).rename_axis('City').reset_index(name='Number of Sellers')
    return city_seller

def create_total_payment_type(df):
    total_payment_type = df.groupby('payment_type')['payment_value'].sum().reset_index()
    return total_payment_type

def create_rfm_df(df):
    today = dt.datetime(2018, 10, 20)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    recency = (today - df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
    frequency = df.groupby('customer_id')['order_id'].count()
    monetary = df.groupby('customer_id')['price'].sum()

    rfm_df = pd.DataFrame({
        'customer_id': recency.index,
        'Recency': recency.values,
        'Frequency': frequency.values,
        'Monetary': monetary.values
    })

    column_list = ['customer_id', 'Recency', 'Frequency', 'Monetary']
    rfm_df.columns = column_list
    return rfm_df

# Set up date filters
min_date = pd.to_datetime(all_df['order_approved_at']).dt.date.min()
max_date = pd.to_datetime(all_df['order_approved_at']).dt.date.max()

# Sidebar setup
with st.sidebar:
    st.image("D:/BANGKIT-ML/submission/dashboard/download.jpg")  # Update path to local image file
    start_date, end_date = st.date_input(
        label='Time Span',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))]

# Create dataframes for visualization
product_count_df = create_product_count_df(main_df)
rating_service_df, max_score = create_rating_service(main_df)
city_customer_df = create_city_customer_df(main_df)
city_seller_df = create_city_seller_df(main_df)
total_payment_type_df = create_total_payment_type(main_df)
rfm_df = create_rfm_df(main_df)

# Dashboard creation
st.title('E-Commerce Public Dataset :moon:')

# Most and Least Sold Products
st.header('Most & Least Product')
col1, col2 = st.columns(2)
with col1:
    most = product_count_df['product_id'].max()
    st.metric('Highest Orders', value=most)
with col2:
    low = product_count_df['product_id'].min()
    st.metric('Lowest Orders', value=low)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english", data=product_count_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=35)
ax[0].set_title("Products with the Highest Sales", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)

sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english", data=product_count_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=35)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Products with the Lowest Sales", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)

plt.suptitle("Most and Least Sold Products", fontsize=58)
st.pyplot(fig)

# Rating Customer by Service
st.header("Rating Customer by Service")
plt.figure(figsize=(16, 8))
sns.barplot(
    x=rating_service_df.index, 
    y=rating_service_df.values, 
    order=rating_service_df.index,
    palette=["#90CAF9" if score == max_score else "#D3D3D3" for score in rating_service_df.index]
)
plt.title("Rating Customers for Service", fontsize=30)
plt.xlabel("Rating", fontsize=18)
plt.ylabel("Customer", fontsize=18)
plt.xticks(fontsize=15)
st.pyplot(plt)

# City with Most Customers and Sellers
st.header('City with Most Customers and Sellers')
tab1, tab2 = st.tabs(['Customers', 'Sellers'])
with tab1:
    st.subheader('Most Customers City')
    top_5_cities_customer = city_customer_df.head(5)
    plt.figure(figsize=(10, 6))
    colors = ["#72BCD4" if city == top_5_cities_customer['City'].iloc[0] else "#D3D3D3" for city in top_5_cities_customer['City']]
    sns.barplot(x="Number of Customers", y="City", data=top_5_cities_customer, hue=top_5_cities_customer['City'], palette=colors, legend=False)
    plt.xlabel('Number of Customers')
    plt.ylabel('City')
    plt.title('Top 5 Cities with the Most Customers', fontsize=20)
    st.pyplot(plt)
with tab2:
    st.subheader('Most Sellers City')
    top_5_cities = city_seller_df.head(5)
    plt.figure(figsize=(10, 6))
    colors = ["#72BCD4" if city == top_5_cities['City'].iloc[0] else "#D3D3D3" for city in top_5_cities['City']]
    sns.barplot(x="Number of Sellers", y="City", data=top_5_cities, hue=top_5_cities['City'], palette=colors, legend=False)
    plt.xlabel('Number of Sellers')
    plt.ylabel('City')
    plt.title('Top 5 Cities with the Most Sellers', fontsize=20)
    st.pyplot(plt)

# Payment Value by Type
st.header('Payment Value by Type')
total_payment_type_df['payment_value_million'] = total_payment_type_df['payment_value'] / 1e6
plt.figure(figsize=(10, 6))
sns.barplot(x="payment_type", y="payment_value_million", data=total_payment_type_df, palette="Blues_d")
plt.xlabel('Payment Type')
plt.ylabel('Total Payment Value (Million)')
plt.title('Total Payment Value by Payment Type', fontsize=20)
fmt = '{x:,.0f}M'
tick = mtick.StrMethodFormatter(fmt)
plt.gca().yaxis.set_major_formatter(tick)
st.pyplot(plt)

# RFM Analysis
st.header("RFM Best Value")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Visualisation based on Recency
sns.barplot(y="Recency", x="customer_id", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), ax=ax[0], color=colors[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id")
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)
ax[0].set_xticks([])

# Visualisation based on Frequency
sns.barplot(y="Frequency", x="customer_id", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), ax=ax[1], color=colors[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('customer_id')
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
ax[1].set_xticks([])

# Visualisation based on Monetary
sns.barplot(y="Monetary", x="customer_id", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), ax=ax[2], color=colors[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel('customer_id')
ax[2].set_title("By Monetary Value", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
ax[2].set_xticks([])

plt.suptitle("Top Customers Based on RFM Values", fontsize=22)
st.pyplot(fig)

#Clustering Analysis
st.header("Clustering")
# Ubah kolom order_purchase_timestamp menjadi datetime, dengan error handling
main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'], errors='coerce')

# Menghitung jumlah transaksi per pelanggan
transaction_counts = main_df.groupby('customer_id')['order_id'].count().reset_index()
transaction_counts.columns = ['customer_id', 'transaction_count']

# Mengelompokkan pelanggan berdasarkan jumlah transaksi
def categorize_transactions(count):
    if count <= 5:
        return 'Low'
    elif count <= 20:
        return 'Medium'
    else:
        return 'High'

transaction_counts['transaction_category'] = transaction_counts['transaction_count'].apply(categorize_transactions)

# Gabungkan kembali dengan data pelanggan
main_df = pd.merge(main_df, transaction_counts[['customer_id', 'transaction_category']], on='customer_id', how='left')

# Binning berdasarkan nilai pembayaran
bins = [0, 100, 500, 1000, float('inf')]
labels = ['Low', 'Medium', 'High', 'Very High']

# Membuat kategori berdasarkan bin
main_df['payment_category'] = pd.cut(main_df['payment_value'], bins=bins, labels=labels, right=False)

# Menghitung minggu dari tanggal pembelian
main_df['week_of_year'] = main_df['order_purchase_timestamp'].dt.isocalendar().week

# Membuat grid untuk tiga grafik dalam satu baris
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Visualisasi 1: Distribusi Kategori Transaksi Pelanggan
sns.countplot(data=main_df, x='transaction_category', palette='Set2', ax=axes[0])
axes[0].set_title('Distribusi Kategori Transaksi Pelanggan')
axes[0].set_xlabel('Kategori Transaksi')
axes[0].set_ylabel('Jumlah Pelanggan')

# Visualisasi 2: Distribusi Kategori Pembayaran
sns.countplot(data=main_df, x='payment_category', palette='Set1', ax=axes[1])
axes[1].set_title('Distribusi Kategori Pembayaran')
axes[1].set_xlabel('Kategori Pembayaran')
axes[1].set_ylabel('Jumlah Transaksi')

# Visualisasi 3: Jumlah Transaksi per Minggu
weekly_transactions = main_df.groupby('week_of_year')['order_id'].count().reset_index()
sns.lineplot(data=weekly_transactions, x='week_of_year', y='order_id', marker='o', color='b', ax=axes[2])
axes[2].set_title('Jumlah Transaksi per Minggu')
axes[2].set_xlabel('Minggu ke-')
axes[2].set_ylabel('Jumlah Transaksi')
axes[2].grid(True)

# Menampilkan semua visualisasi
st.pyplot(fig)
