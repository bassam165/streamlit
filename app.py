import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# Service account configuration
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "sigma-cairn-449113-e2",
    "private_key_id": "b0bc7cbcdc58ead6d81c81127dee666fbbfe31bd",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDS3zmkowGAB6i7
PIw5tgfcy3k9f/SPt8kGZ8GvArE02tW01XUsald3jo5lSBmNmxg1JTwicNiyV82y
69KUqFq8SzffhRnLvi6zyJJgzsfT2sfGQ3oeLSzXXwUyR7kKFgmd/yhua4YDS1Qa
BiIF8mz6asEBU5gOjYIIYZzk280L3hsgZCPhfbyt6oz9P+z+LlEZJHXDM2EPynNC
aXAHDEJVoMAkm/LBmpklCLaYTclnZA8yudHmTZkMk8h2dOZrbT5BdXTXygLKsQYB
x+VFMuxfm22eKW0MC8EjZjX3tZahi8oFWfEnET0edJnkRFobpNjfoT84/deE8JGT
KB7Uysf9AgMBAAECggEALk30Q3HD55BG/e56wEV3joVjtxx84H4z92MbRcnqjbes
C8x/sWQcltVH8XeWnOC8vRbTEKEFBIyBT9O25wvc+NHvj/aTRokZikL12aoueRfm
nGO+0heLbDOiWXskZ9GVBQu9nhmgUOLeseQ83l9wjMCaZycrEa8DKcH9iMe3S+5w
PrxM3AA29I2k6XsZTyglacksDFVmUoUyz7XPkFFHjV+Glgh3fjhFM9TdtYXeoOr0
n7/+LfaQUMBZApHLpyz4JQerk63EqwnhUyMwzhMo8h5H68ewxf18anx0/qPGBmXO
4qAkgVtPNHN7NbZQl+fLl7exLev48MvhGpUaNoMSwQKBgQD+0yF1HZKnyyVhmJzL
SN5gQDugl9tqCALzwzskQin8p8spleI5DHN0jztnxsMbMW5UDBgY6NlWizqHADL3
l31g/tX+Huq7gD9eFlbAEKRUOs1nQq+NiR+5frGAdfYz+DBm24gSeiqteL18JXnl
0KXx3j5vke4FPyRYQMSW6YNAzQKBgQDT2DMpAVePHhFVUb7Hg5WOcLoxcvi2J9x3
GiD8KVcu4T4rdVuKqVzyYhIWgn7QCAAy9uAXfEaXOmmboqTxJBUpczm34G21P1V9
Wb3jPUYxcYrDqmmNAx84FUIs8JOYWGukMRzdkEgWcCQGncPrmWJsIN4E1JlCxhOh
XGHqcNnj8QKBgQCr3mbQgNOrTD64JqCKE2m47VnKJOIeD60+D81R1TZQbDOAptDf
vWAZm4lrowlwy9Qn58hQ9KuxzVH6P84gZBJyWy6lqOCU+hjDMrnr7M2I6egj3zxc
b8Hv8F1z0RvvTVQH68VJARDL04Wpt/URZbqm+UiPI5OwAjhXNcfiKTkXeQKBgGvn
xjduzZDCugWBe/HYXoeNd+nULEdsimnIT2DiFdx1MtukDZrVpdh4h8obcki4qpFL
Gt4bmUFSqZRzBh0mSfkxDgdRM9CMkBknaweioGxy70G3Pchr/KzudyS47hU9hKa/
tXpOEcoMGO2d0rvhBzcYjr5bJC3VAw7AJcfq77GhAoGBALeEH9BkVGzquQDfEkVZ
Oj24gHzxJZk8B3kOa6xGOWbEctZCZfWdf6j9mcwXcRQhu/aqHvWB1cjslrfxiNZV
xRAgYzfPwSfHwcjLvXFuZn7UpRDtOyx7Oof1KRdI65beLmNsgnXRwIEBxURIiHO5
5IuPOsjmLT+wcADC+k1DYz2n
-----END PRIVATE KEY-----""",
    "client_email": "react-api@sigma-cairn-449113-e2.iam.gserviceaccount.com",
    "client_id": "114898407444799135839",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/react-api%40sigma-cairn-449113-e2.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Configure Google Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=SCOPES
)
gc = gspread.authorize(credentials)

def create_new_spreadsheet(title, user_email):
    try:
        spreadsheet = gc.create(title)
        # Share with user's email for visibility
        spreadsheet.share(user_email, perm_type='user', role='writer')
        # Initialize header row
        worksheet = spreadsheet.sheet1
        worksheet.append_row(["Date", "Description", "Amount", "Category"])
        return spreadsheet
    except Exception as e:
        st.error(f"Error creating spreadsheet: {e}")
        return None

def add_entry_to_sheet(spreadsheet, entry):
    try:
        worksheet = spreadsheet.sheet1
        worksheet.append_row(entry)
        return True
    except Exception as e:
        st.error(f"Error adding entry: {e}")
        return False

def get_sheet_data(spreadsheet):
    try:
        worksheet = spreadsheet.sheet1
        records = worksheet.get_all_records()
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return pd.DataFrame()

# Streamlit app
st.title("Google Sheets Financial Tracker 📊")

tab1, tab2, tab3 = st.tabs(["Create New Sheet", "Add Entry", "View Data"])

with tab1:
    st.header("Create New Spreadsheet")
    new_sheet_name = st.text_input("Enter spreadsheet name")
    user_email = st.text_input("Your Google account email for access")
    if st.button("Create New Sheet"):
        if new_sheet_name and user_email:
            new_spreadsheet = create_new_spreadsheet(new_sheet_name, user_email)
            if new_spreadsheet:
                st.success(f"Spreadsheet '{new_spreadsheet.title}' created successfully!")
                st.write(f"URL: {new_spreadsheet.url}")
                st.markdown("**Check your Google Drive after creation - it may take a few moments to appear**")
        else:
            st.warning("Please enter both spreadsheet name and your email")

with tab2:
    st.header("Add New Entry")
    spreadsheets = gc.openall()
    if spreadsheets:
        selected_sheet = st.selectbox("Select Spreadsheet", [sh.title for sh in spreadsheets])
        spreadsheet = gc.open(selected_sheet)
        
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Rent", "Other"])
        
        if st.button("Add Entry"):
            entry = [
                str(date),
                description,
                str(amount),
                category
            ]
            if add_entry_to_sheet(spreadsheet, entry):
                st.success("Entry added successfully!")
    else:
        st.warning("No spreadsheets found. Create one first!")

with tab3:
    st.header("View Data")
    spreadsheets = gc.openall()
    if spreadsheets:
        selected_sheet = st.selectbox("Select Spreadsheet to View", [sh.title for sh in spreadsheets])
        spreadsheet = gc.open(selected_sheet)
        df = get_sheet_data(spreadsheet)
        
        if not df.empty:
            try:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                
                st.subheader("Filter Data")
                timeframe = st.selectbox("Select Timeframe", ["All", "Daily", "Monthly", "Yearly"])
                
                if timeframe == "Daily":
                    selected_date = st.date_input("Select Date")
                    filtered_df = df[df['Date'] == selected_date]
                elif timeframe == "Monthly":
                    month = st.selectbox("Month", range(1, 13), format_func=lambda x: datetime(1900, x, 1).strftime('%B'))
                    year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year)
                    filtered_df = df[(df['Date'].apply(lambda x: x.month) == month) & 
                                    (df['Date'].apply(lambda x: x.year) == year)]
                elif timeframe == "Yearly":
                    year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year)
                    filtered_df = df[df['Date'].apply(lambda x: x.year) == year]
                else:
                    filtered_df = df
                
                st.subheader("Financial Records")
                st.dataframe(filtered_df)
                
                st.subheader("Summary")
                if not filtered_df.empty:
                    total_amount = filtered_df['Amount'].astype(float).sum()
                    st.metric("Total Amount", f"${total_amount:.2f}")
            except KeyError:
                st.error("Invalid sheet format - please use sheets created by this app")
        else:
            st.warning("No data found in the selected spreadsheet")
    else:
        st.warning("No spreadsheets available. Create one first!")