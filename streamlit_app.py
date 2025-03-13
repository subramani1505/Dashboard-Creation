import pandas as pd
import streamlit as st
import plotly.express as px

# Load and clean data
df = pd.read_csv(r"C:\Users\subramani.v\Documents\zomato_accounts_payable.csv")
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
df['Due Date'] = pd.to_datetime(df['Due Date'])
df['Payment Date'] = pd.to_datetime(df['Payment Date'])
df['Days Overdue'] = df['Days Overdue'].apply(lambda x: max(0, x))

# Dashboard title
st.title("Zomato Accounts Payable Dashboard")

# Key metrics cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Payables", f"₹{df['Invoice Amount'].sum():,.2f}")
col2.metric("Overdue Amount", f"₹{df[df['Payment Status'] == 'Overdue']['Invoice Amount'].sum():,.2f}")
col3.metric("Avg Payment Days", f"{(df['Payment Date'] - df['Invoice Date']).dt.days.mean():.1f}")

# Vendor Analysis
st.subheader("Vendor Analysis")
col1, col2 = st.columns(2)
with col1:
    top_vendors = df.groupby('Vendor Name', as_index=False)['Invoice Amount'].sum().nlargest(10, 'Invoice Amount')
    fig1 = px.bar(top_vendors, x='Vendor Name', y='Invoice Amount', title='Top 10 Vendors by Invoice Amount')
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.pie(df, names='Vendor Category', values='Invoice Amount', title='Vendor Category Distribution')
    st.plotly_chart(fig2, use_container_width=True)

# Payment Status
st.subheader("Payment Status")
col1, col2 = st.columns([1, 2])
with col1:
    fig3 = px.pie(df, names='Payment Status', values='Invoice Amount', title='Payment Status Distribution')
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.subheader("Overdue Invoices")
    overdue_df = df[df['Payment Status'] == 'Overdue'][['Vendor Name', 'Invoice Amount', 'Days Overdue']]
    st.dataframe(overdue_df, hide_index=True, use_container_width=True)

# Trends
st.subheader("Monthly Payables Trend")
monthly_df = df.groupby(pd.Grouper(key='Invoice Date', freq='M'))['Invoice Amount'].sum().reset_index()
fig4 = px.line(monthly_df, x='Invoice Date', y='Invoice Amount', title='Monthly Payables')
st.plotly_chart(fig4, use_container_width=True)