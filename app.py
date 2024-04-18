import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pytz import UTC
import plotly.express as px
import os
st.set_page_config(page_title="HYDERABAD STORE", page_icon=":racing_motorcycle:",layout="wide")
st.title("HYDERABAD STORE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Define the scope
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
df = pd.DataFrame(data[1:], columns=data[0])

# Preprocessing data
df['Cancelled At'] = pd.to_datetime(df['Cancelled At'])
df.drop(df[df['Cancelled At'].notnull()].index, inplace=True)
df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')
df['Created At'] = pd.to_datetime(df['Created At'])
# Drop rows with 'Sales Person' as 'Superman test' from the original DataFrame
df.drop(df[df['Sales Person'] == 'Superman test'].index, inplace=True)
df.drop(df[df['Sales Person'] == ''].index, inplace=True)

st.write(df)

col1, col2 = st.columns((2))
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
    df_filtered = df.copy()
elif Email and not Sales_Person:
    df_filtered = df[df["Email"].isin(Email)]
elif Sales_Person and not Email:
    df_filtered = df[df["Sales Person"].isin(Sales_Person)]
else:
    df_filtered = df[df["Email"].isin(Email) & df["Sales Person"].isin(Sales_Person)]


# Convert "Total Price" column to numeric
df_filtered['Total Price'] = pd.to_numeric(df_filtered['Total Price'], errors='coerce')

# Grouping the data by salesperson and summing up the total sales
salesperson_sales = df_filtered.groupby('Sales Person')['Total Price'].sum()

# Convert the 'Order Date' column to datetime if it's not already
df_filtered['Created At'] = pd.to_datetime(df_filtered['Created At'])

# Grouping the data by date and salesperson, and summing up the total sales for each day and each salesperson
daily_sales_by_salesperson = df_filtered.groupby([df_filtered['Created At'].dt.date, 'Sales Person'])['Total Price'].sum()

# Streamlit App
st.title('Sales Dashboard')

# Displaying the total sales by salesperson
st.subheader("Sales Person Wise:")
st.write(salesperson_sales)

# Displaying the daily sales by salesperson
st.subheader("Daily Sales by Salesperson:")
st.write(daily_sales_by_salesperson)


# Display filtered DataFrame
st.dataframe(df_filtered)


total_price = df_filtered['Total Price'].sum()

st.write(f"Total Price :{total_price}")