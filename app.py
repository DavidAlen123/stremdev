import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pytz import UTC
import local

# Set page configuration
st.set_page_config(
    page_title="HYDERABAD STORE",
    page_icon=":racing_motorcycle:",
    layout="wide"
)

# Define the scope for Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Define the credentials
credentials = {
    "type": "service_account",
    "project_id": "solar-haven-307711",
    "private_key_id": "38d9bf04a9dd340e278a6f4d30bf4d15027f16d3",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYzfd14oCERH3y\nElNgD7HiqbFCnGNvX9T/jYREijWyWV/u5b7vuHOrudES/7l1PiAogUsfZNdL4gZx\nP2+SCHgNG5NAevDOzfromaEr5denbs6Q0Eiyv0XruHffk7P42J28NmWV3XK19wiK\nqS4rgUGKmTCfokgDzJm77IZB7nualGj5EznYAWVI8pko6UwGFVZ7LPgLStOuuIGZ\n9Td+rqyHj8nv5q6cwcNX2kpoI1dLtxuc34pkOhVk3O9Wvw/9rnKYpb2Bt1pvCorv\niWzKM+v2JkENziGQ4OV2dANletbIcRBLbCXRrxO1xVmUTd0ySgH6IhnrEt5/EiJu\nCcnPkPABAgMBAAECggEACK1drSMun5yaKdkf6yVVqku+Y3sc47VDMiM42wFpGsVG\n+KnLVY7dWk8qlgcUJiQhZ12dYxlHIKtgNKIkVgTuwR+MajVBdBV8aFjVwYsGcZYW\nwGcFsdnD86ZDbfhcaKZK0eCfejsNv0iu19XjmiwnMmPlNU5qcXR75rCVwwfHfK1H\nE2VBbYgDhcnv3vgXz4cTOIqfDujsLkJUQh4XTeuoToB+iGqbg8mubEsWBXQUUkwN\nfoE7McTj9zZvcwOKD5vGraliwiUlbtFJHFkyThGytt1AGIt8YW6tPsJI1AibXfYq\n50dIOjV6JO67xozbEHTS6AoI+Ikis+le8SNKi4HeUQKBgQD0RlGDft3VemjohIKc\nuLTdKbIgFGsXfG7MtWmQTpBX4dDjE0d0NDwA/SL0Qxs8X4uOKBZIa1hpxcKZC3zq\nld5vbYqfk+VvAG0Cx4KeDjPioRdAwH6ZEwkgP6zeCJNkTafCkHtA8GJMjB5iySQv\n+cYDXVkZNQD1tu2Bc8pWDpaiHQKBgQDjNhdrtNaNMN84HhwLLd0hnW04C/UAsU+c\nDyltmpoQHjOHOWyU19zkzxnhRFnRGgE3IAAKJWDE46zdbHFgVyOgQjr9kno4V84L\njyhqR6mu5savUMR2ip9j3bd5EjLy9gAqvx6eRMgCj1yGbjAO4tXYExRx94xGLbxP\nh/AJyCjgNQKBgQCBp0Uit1bFNWizaYnt5zfQX4406sGAwMIKk4uJVbnVe30k2ZnG\neucSW0mPPoMZQ1lORca1/4v48Ed+dhOCa7OZjxnR420WwrIZlI2mmME/W+N8se9A\nDlN8s29slj6tMW6Gnatd53k1SfXi1wIHGNrZ9FUTRQfSY5qiaDQQA0Q+nQKBgA9g\nMreMNlS5sPFoQDeVc/h5YdHAJWVVmnCSKhiLtM9Qa+ZDwZBVB1LInRS8fmODIf/r\n/3SwUNsiGSmm1AlT/Eo1ES7lwbWcY4outupyTQ5T+bAVhCYNfXnRoD/mNmJwuVQr\nONQ3DV32+6jxPflT6mrD58dKnEiHgc3UAi93RyTdAoGAR9057eBWcHbQfLy4AZ3H\n2L2Su6UsYQOJhFn+b7IkSon/WAwJLGTYFQjpoz3fi9xZiMzfQEEJJEq/966/nJTf\nrbPNAVdyBBCFOqQpmbz2FTpBSwwQTba65xSgyHMgtpLg9SfZ2t1g1Ocqm+PA8QDo\nhJSZRrmwzwx+KDx81P2EvR4=\n-----END PRIVATE KEY-----\n",
    "client_email": "inventory-tracker@solar-haven-307711.iam.gserviceaccount.com",
    "client_id": "104221851914321462233",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/inventory-tracker%40solar-haven-307711.iam.gserviceaccount.com"
}

# Authenticate with credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(credentials)

# Open the Google Spreadsheet by its ID
spreadsheet_id = "1trGCOTGaNyBYUzp31XPCLCPY3SWv6_XGU_sMTextvJs"
spreadsheet = client.open_by_key(spreadsheet_id)

# Access a specific worksheet
worksheet = spreadsheet.sheet1

data = worksheet.get_all_values()

# Assuming 'data' is a list of lists where the first list contains column names
df = pd.DataFrame(data[1:], columns=data[0])
df['Cancelled At'] = pd.to_datetime(df['Cancelled At'])

df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')


# Convert the Quantity column to numeric
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Set the locale to Indian English
locale.setlocale(locale.LC_NUMERIC, 'en_IN')

# Define a function to format numbers in Indian format
def format_indian_format(num):
    return locale.format_string("%.2f", num, grouping=True)

# Apply the formatting function to the 'Total Price' column
df['Total Price'] = df['Total Price'].apply(format_indian_format)
df['Unit Price'] = df['Unit Price'].apply(format_indian_format)
# Convert the Quantity column to numeric
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')





st.write(df)

# Drop rows with specific salesperson names
df.drop(df[df['Sales Person'] == 'Superman test'].index, inplace=True)
df.drop(df[df['Sales Person'] == ''].index, inplace=True)
df.drop(df[df['Sales Person'] == 'Subash Bose'].index, inplace=True)

col1, col2 = st.sidebar.columns((2))
df["Created At"] = pd.to_datetime(df["Created At"])

startDate = pd.to_datetime(df["Created At"]).min()
endDate = pd.to_datetime(df["Created At"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Convert input dates to datetime objects
date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)

# Convert input dates to the timezone of the DataFrame's "Created At" column
date1 = date1.tz_localize(UTC)
date2 = date2.tz_localize(UTC)

# Filter the DataFrame
date_filter = df[(df["Created At"] >= date1) & (df["Created At"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

Email = st.sidebar.multiselect("Select Customer Email", df["Email"].unique())
Sales_Person = st.sidebar.multiselect("Select Sales_Person", df["Sales Person"].unique())

# Apply filters
if not Email and not Sales_Person:
    df_filtered = date_filter.copy()
elif Email and not Sales_Person:
    df_filtered = date_filter[date_filter["Email"].isin(Email)]
elif Sales_Person and not Email:
    df_filtered = date_filter[date_filter["Sales Person"].isin(Sales_Person)]
else:
    df_filtered = date_filter[date_filter["Email"].isin(Email) & df["Sales Person"].isin(Sales_Person)]

# Create separate dataframes for cancelled and non-cancelled orders
df_filtered['Total Price'] = pd.to_numeric(df_filtered['Total Price'], errors='coerce')
cancelled_orders = df_filtered[df_filtered["Cancelled At"].notnull()]
non_cancelled_orders = df_filtered[df_filtered["Cancelled At"].isnull()]

# Grouping the data by salesperson and summing up the total sales for each group
cancelled_sales = cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index()
non_cancelled_sales = non_cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index()

# Merge the two dataframes on 'Sales Person'
merged_sales = pd.merge(cancelled_sales, non_cancelled_sales, on='Sales Person', suffixes=('_Cancelled', '_Non_Cancelled'))

# Calculate total amount of canceled orders for each salesperson
cancelled_orders_total_amount = cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index(name='Total Amount Cancelled')

# Calculate total number of cancelled orders for each salesperson
cancelled_orders_count = cancelled_orders.groupby('Sales Person').size().reset_index(name='Total Orders Cancelled')

# Calculate total amount of non-cancelled orders for each salesperson
non_cancelled_orders_total_amount = non_cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index(name='Sales Amount')

# Calculate total number of non-cancelled orders for each salesperson
non_cancelled_orders_count = non_cancelled_orders.groupby('Sales Person').size().reset_index(name='Total Sales')

# Merge total amount and total number of Sales orders
sale_data = non_cancelled_orders_count.merge(non_cancelled_orders_total_amount, on='Sales Person')

# Merge total amt and total number of cancel order
cancel_data = cancelled_orders_count.merge(cancelled_orders_total_amount, on='Sales Person')


# Display non-cancelled order details
st.subheader("Sales Order Details:")
st.write(non_cancelled_orders)

st.subheader("Cancel Order Details:")
st.write(cancelled_orders)


col1,col2 = st.columns(2)
with col1:
    # Display the Sales data
    st.subheader("Sales Order Summary:")
    st.write(sale_data)
with col2:
    # Display the Cancel data
    st.subheader("Cancelled Order Summary:")
    st.write(cancel_data)


# Calculate total price for each selected SKU
total_price_per_sku = df_filtered.groupby('SKU')['Total Price'].sum().reset_index(name='Total Price')


# Add a dropdown widget for selecting the number of top SKUs
top_sku_count = st.sidebar.selectbox("Select the Number of Top SKUs", [10, 50, 100, 150, 200])

# Sort the grouped DataFrame in descending order based on total sales
top_sku_sales = total_price_per_sku.sort_values(by='Total Price', ascending=False).head(top_sku_count)


# Group the data by SKU and sum up the total price and quantity for each SKU
sku_summary = df_filtered.groupby('SKU').agg({'Total Price': 'sum', 'Quantity': 'sum', 'Title': 'first', 'Vendor': 'first','Created At':'first'}).reset_index()

# Sort the grouped DataFrame in descending order based on total sales
top_sku_sales = sku_summary.sort_values(by='Total Price', ascending=False).head(top_sku_count)

# Display the top SKUs with quantity, title, vendor, and total price
st.subheader(f"Top {top_sku_count} SKUs with Highest Sales:")
st.write(top_sku_sales[['SKU','Created At','Title', 'Vendor', 'Quantity', 'Total Price']])


#####################################################################3


# Calculate total price for each selected SKU
vendor_wise_sale_total = df_filtered.groupby('Vendor')['Total Price'].sum().reset_index(name='Total Price')


# Add a dropdown widget for selecting the number of top SKUs
top_vendor_count = st.sidebar.selectbox("Select the Number of Top Vendor's", [10, 50, 100, 150, 200])

# Sort the grouped DataFrame in descending order based on total sales
top_vendor_sales = vendor_wise_sale_total.sort_values(by='Total Price', ascending=False).head(top_vendor_count)

# Group the data by SKU and sum up the total price and quantity for each SKU
vendor_summary = df_filtered.groupby('Vendor').agg({'Total Price': 'sum', 'Quantity': 'sum', 'Title': 'first','SKU':'first', 'Created At':'first' }).reset_index()

# Sort the grouped DataFrame in descending order based on total sales
top_vendor_sales = vendor_summary.sort_values(by='Total Price', ascending=False).head(top_vendor_count)

# Display the top SKUs with quantity, title, vendor, and total price
st.subheader(f"Top {top_vendor_count} Vendor's with Highest Sales:")
st.write(top_vendor_sales[['Vendor', 'Created At','Title','SKU', 'Quantity', 'Total Price']])



import plotly.express as px

# Visualize Sales Order Summary
fig1 = px.bar(sale_data, x='Sales Person', y='Sales Amount', title='Sales Amount by Sales Person')
st.plotly_chart(fig1)

# Visualize Cancelled Order Summary
fig2 = px.bar(cancel_data, x='Sales Person', y='Total Amount Cancelled', title='Cancelled Amount by Sales Person')
st.plotly_chart(fig2)

# Visualize Top SKUs with Highest Sales
fig3 = px.bar(top_sku_sales, x='SKU', y='Total Price', title=f'Top {top_sku_count} SKUs with Highest Sales')
st.plotly_chart(fig3)

# Visualize Top Vendors with Highest Sales
fig4 = px.bar(top_vendor_sales, x='Vendor', y='Total Price', title=f'Top {top_vendor_count} Vendors with Highest Sales')
st.plotly_chart(fig4)























