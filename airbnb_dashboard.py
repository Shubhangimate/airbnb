import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(layout="wide", page_title="Airbnb Berlin Analysis")

# Title
st.title("🏠 Airbnb Berlin Data Dashboard")
st.markdown("Explore trends in prices, room types, neighborhoods, and more!")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("listings.csv")
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df = df[df['price'] < 500]  # filter extreme values
    df['beds'] = df['beds'].fillna(0)
    df['bathrooms'] = df['bathrooms'].fillna(0)
    return df

df = load_data()
df['neighbourhood'] = df['neighbourhood'].astype(str)


# Sidebar filters
st.sidebar.header("🔎 Filters")
neighs = st.sidebar.multiselect("Select Neighborhood(s):", options=sorted(df['neighbourhood'].unique()), default=df['neighbourhood'].unique())
room_types = st.sidebar.multiselect("Select Room Type(s):", options=df['room_type'].unique(), default=df['room_type'].unique())

filtered = df[(df['neighbourhood'].isin(neighs)) & (df['room_type'].isin(room_types))]

# Layout in columns
col1, col2 = st.columns(2)

# Q1: Price Distribution
with col1:
    st.subheader("💸 Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered['price'], bins=40, kde=True, ax=ax)
    st.pyplot(fig)

# Q2: Average Price by Neighborhood
with col2:
    st.subheader("🏙️ Avg Price by Neighborhood")
    avg_price = filtered.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=avg_price.index, y=avg_price.values, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Q3: Room Type vs Price (Boxplot)
st.subheader("🛏️ Room Type vs Price")
fig, ax = plt.subplots()
sns.boxplot(data=filtered, x='room_type', y='price', ax=ax)
st.pyplot(fig)

# Q4: Superhost Pricing
if 'host_is_superhost' in filtered.columns:
    st.subheader("🌟 Superhost vs Price")
    fig, ax = plt.subplots()
    sns.violinplot(x='host_is_superhost', y='price', data=filtered, ax=ax)
    st.pyplot(fig)

# Q5: Reviews vs Price
st.subheader("💬 Reviews vs Price")
fig, ax = plt.subplots()
sns.scatterplot(x='number_of_reviews', y='price', data=filtered, ax=ax)
st.pyplot(fig)

# Q6: Beds & Bathrooms Heatmap
st.subheader("🛁 Beds and Bathrooms vs Price")
pivot = filtered.pivot_table(values='price', index='beds', columns='bathrooms', aggfunc='mean')
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data: Airbnb Berlin")
