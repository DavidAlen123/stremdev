import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pytz import UTC

# Initialize session state
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Create an instance of SessionState
session_state = SessionState(authenticated=False)
@st.cache(allow_output_mutation=True)
def get_session_state():
    return session_state

# Set page configuration
st.set_page_config(
    page_title="HYDERABAD STORE",
    page_icon=":racing_motorcycle:",
    layout="wide"
)

# Authenticate users
def authenticate():
    session_state = get_session_state()
    if not session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        users = {
            "david": "123",
            "mark": "456",
            "alen": "789"
        }

        if st.button("Login"):
            if username in users and password == users[username]:
                session_state.authenticated = True
                return True
            else:
                st.error("Invalid username or password")
                return False
    else:
        return True

def logout():
    session_state = get_session_state()
    session_state.authenticated = False


# Check authentication status
is_authenticated = authenticate()


# Display content based on authentication status
if is_authenticated:
    st.sidebar.write("You are logged in.")
    # Add authenticated user-specific content here
    def main():
        scope = ["https://www.googleapis.com/auth/spreadsheets"]

        # Retrieve credentials from Streamlit secrets
        credentials = {
         
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

        df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
        # Set the locale to Indian English

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
        cancelled_orders = df_filtered[df_filtered["Cancelled At"].notnull()]

        non_cancelled_orders = df_filtered[df_filtered["Cancelled At"].isnull()]

        # Define a function to format numbers in Indian format

        # Grouping the data by salesperson and summing up the total sales for each group
        cancelled_sales = cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index()

        non_cancelled_sales = non_cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index()

        # Merge the two dataframes on 'Sales Person'
        merged_sales = pd.merge(cancelled_sales, non_cancelled_sales, on='Sales Person',
                                suffixes=('_Cancelled', '_Non_Cancelled'))

        # Calculate total amount of canceled orders for each salesperson
        cancelled_orders_total_amount = cancelled_orders.groupby('Sales Person')['Total Price'].sum().reset_index(
            name='Total Amount Cancelled')

        # Calculate total number of cancelled orders for each salesperson
        cancelled_orders_count = cancelled_orders.groupby('Sales Person').size().reset_index(
            name='Total Orders Cancelled')

        # Calculate total amount of non-cancelled orders for each salesperson
        non_cancelled_orders_total_amount = non_cancelled_orders.groupby('Sales Person')[
            'Total Price'].sum().reset_index(
            name='Sales Amount')

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

        col1, col2 = st.columns(2)
        with col1:
            # Display the Sales data
            st.subheader("Sales Order Summary:")
            st.write(sale_data)
        with col2:
            # Display the Cancel data
            st.subheader("Cancelled Order Summary:")
            st.write(cancel_data)

        # Calculate total price for each selected SKU
        # Filter out cancelled orders from the original DataFrame
        df_filtered_non_cancelled = df_filtered[df_filtered['Cancelled At'].isnull()]

        # Group the data by SKU and sum up the total price and quantity for each SKU
        sku_summary = df_filtered_non_cancelled.groupby('SKU').agg(
            {'Total Price': 'sum', 'Quantity': 'sum', 'Title': 'first', 'Vendor': 'first', 'Created At': 'first',
             'Cancelled At': 'first'}).reset_index()

        # Add a dropdown widget for selecting the number of top SKUs
        top_sku_count = st.sidebar.selectbox("Select the Number of Top SKUs", [10, 50, 100, 150, 200])

        # Sort the grouped DataFrame in descending order based on total sales
        top_sku_sales = sku_summary.sort_values(by='Total Price', ascending=False).head(top_sku_count)

        # Display the top SKUs with quantity, title, vendor, and total price
        st.subheader(f"Top {top_sku_count} SKUs with Highest Sales:")
        st.write(top_sku_sales[['SKU', 'Quantity', 'Total Price']])

        #####################################################################3

        # Calculate total price for each selected SKU from non-cancelled orders
        vendor_wise_sale_total = df_filtered_non_cancelled.groupby('Vendor')['Total Price'].sum().reset_index(
            name='Total Price')

        # Add a dropdown widget for selecting the number of top vendors
        top_vendor_count = st.sidebar.selectbox("Select the Number of Top Vendors", [10, 50, 100, 150, 200])

        # Sort the grouped DataFrame in descending order based on total sales
        top_vendor_sales = vendor_wise_sale_total.sort_values(by='Total Price', ascending=False).head(top_vendor_count)

        # Group the data by vendor and retrieve other relevant information
        vendor_summary = df_filtered_non_cancelled.groupby('Vendor').agg(
            {'Total Price': 'sum', 'Quantity': 'sum', 'Title': 'first', 'SKU': 'first', 'Created At': 'first',
             'Cancelled At': 'first'}).reset_index()

        # Sort the grouped DataFrame in descending order based on total sales

        top_vendor_sales = vendor_summary.sort_values(by='Total Price', ascending=False).head(top_vendor_count)

        # Display the top vendors with quantity, title, SKU, total price, and cancelled at information
        st.subheader(f"Top {top_vendor_count} Vendors with Highest Sales:")
        st.write(top_vendor_sales[['Vendor', 'Title', 'Total Price']])

        import plotly.express as px

        # Visualize Sales Order Summary
        fig1 = px.bar(sale_data, x='Sales Person', y='Sales Amount', title='Sales Amount by Sales Person')
        st.plotly_chart(fig1)

        # Visualize Cancelled Order Summary
        fig2 = px.bar(cancel_data, x='Sales Person', y='Total Amount Cancelled',
                      title='Cancelled Amount by Sales Person')
        st.plotly_chart(fig2)

        # Visualize Top SKUs with Highest Sales
        fig3 = px.bar(top_sku_sales, x='SKU', y='Total Price', title=f'Top {top_sku_count} SKUs with Highest Sales')
        st.plotly_chart(fig3)

        # Visualize Top Vendors with Highest Sales
        fig4 = px.bar(top_vendor_sales, x='Vendor', y='Total Price',
                      title=f'Top {top_vendor_count} Vendors with Highest Sales')
        st.plotly_chart(fig4)


    if __name__ == "__main__":
        main()

    if st.sidebar.button("Logout"):
        logout()
        st.success("You have been logged out.")
        st.experimental_rerun()
        
else:
    st.write("You are not logged in.")
