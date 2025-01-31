import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
from fpdf import FPDF
from io import BytesIO

# ----------------------------------
# SERVICE ACCOUNT / GOOGLE SHEETS SETUP
# ----------------------------------
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

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=SCOPES
)
gc = gspread.authorize(credentials)

# ----------------------------------
# GOOGLE SHEET HELPER FUNCTIONS
# ----------------------------------
def create_new_spreadsheet(title, user_email):
    """
    Create a new spreadsheet, share with user_email, and
    initialize a header row with 7 columns.
    """
    try:
        spreadsheet = gc.create(title)
        spreadsheet.share(user_email, perm_type='user', role='writer')
        worksheet = spreadsheet.sheet1
        
        # Enforce these columns to avoid duplicates
        worksheet.append_row(["Date", "Description", "Buying Price",
                              "Selling Price", "Revenue", "Category", "Memo"])
        return spreadsheet
    except Exception as e:
        st.error(f"Error creating spreadsheet: {e}")
        return None

def add_entry_to_sheet(spreadsheet, entry):
    """
    Append a new transaction (row) to the spreadsheet.
    """
    try:
        worksheet = spreadsheet.sheet1
        worksheet.append_row(entry)
        return True
    except Exception as e:
        st.error(f"Error adding entry: {e}")
        return False

def get_sheet_data(spreadsheet):
    """
    Reads all values (including the first row). Then manually
    assigns known column names to avoid duplicates or misalignment.
    Ensures numeric columns are properly converted to floats.
    """
    try:
        worksheet = spreadsheet.sheet1
        data = worksheet.get_all_values()  # returns a list of lists
        
        # If only header row or no data, return empty DataFrame
        if len(data) <= 1:
            return pd.DataFrame(columns=["Date", "Description", "Buying Price",
                                         "Selling Price", "Revenue", "Category", "Memo"])
        
        # We assume the columns are in this exact order:
        columns = ["Date", "Description", "Buying Price", "Selling Price", "Revenue", "Category", "Memo"]
        
        df = pd.DataFrame(data[1:], columns=columns)
        
        # Convert numeric columns to float, invalid parsing => NaN => fill with 0
        df["Buying Price"]  = pd.to_numeric(df["Buying Price"],  errors="coerce").fillna(0)
        df["Selling Price"] = pd.to_numeric(df["Selling Price"], errors="coerce").fillna(0)
        df["Revenue"]       = pd.to_numeric(df["Revenue"],       errors="coerce").fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return pd.DataFrame()

# ----------------------------------
# PDF GENERATION
# ----------------------------------
class PDFReport(FPDF):
    """Simple FPDF subclass for table printing."""
    pass

def generate_single_transaction_pdf(transaction):
    """
    Generate a PDF (as an FPDF object) containing details for
    one newly-added transaction.
    
    transaction: [Date, Description, Buying, Selling, Revenue, Category, Memo]
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Single Transaction Receipt", ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    fields = ["Date", "Description", "Buying Price", "Selling Price", "Revenue", "Category", "Memo"]
    
    pdf.ln(5)
    for field_name, field_value in zip(fields, transaction):
        pdf.cell(50, 10, f"{field_name}:", 0)
        pdf.cell(0, 10, str(field_value), 0, ln=1)
    
    return pdf

def generate_pdf_report(dataframe, timeframe, selected_date=None, month=None, year=None):
    """
    Generates an FPDF object of multiple transactions (filtered by the user),
    plus a summary of totals.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Financial Report", ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    
    # Show timeframe info
    if timeframe != "All":
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Timeframe: {timeframe}", ln=True)
        pdf.set_font("Arial", size=12)
        
        if timeframe == "Daily" and selected_date:
            pdf.cell(0, 10, f"Date: {selected_date}", ln=True)
        elif timeframe == "Monthly" and month and year:
            pdf.cell(0, 10,
                     f"Month: {datetime(1900, month, 1).strftime('%B')} {year}",
                     ln=True)
        elif timeframe == "Yearly" and year:
            pdf.cell(0, 10, f"Year: {year}", ln=True)
    
    pdf.ln(5)
    # Table headers
    col_widths = [25, 45, 25, 25, 25, 25, 30]  # Adjust as you wish
    headers = ["Date", "Description", "Buying Price", "Selling Price",
               "Revenue", "Category", "Memo"]
    
    # Print table header
    for i, header in enumerate(headers):
        pdf.set_font("Arial", "B", 10)
        pdf.cell(col_widths[i], 8, header, border=1, ln=0)
    pdf.ln(8)
    
    # Print each transaction row
    pdf.set_font("Arial", size=10)
    for _, row in dataframe.iterrows():
        row_values = [
            str(row["Date"]),
            str(row["Description"]),
            f"{row['Buying Price']:.2f}",
            f"{row['Selling Price']:.2f}",
            f"{row['Revenue']:.2f}",
            str(row["Category"]),
            str(row["Memo"])[:30]  # truncate if it's very long
        ]
        for i, val in enumerate(row_values):
            pdf.cell(col_widths[i], 8, val, border=1, ln=0)
        pdf.ln(8)
    
    # Summary Section
    pdf.ln(10)
    total_buying = dataframe['Buying Price'].sum()
    total_selling = dataframe['Selling Price'].sum()
    total_revenue = dataframe['Revenue'].sum()
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Total Buying Price:  ${total_buying:.2f}", ln=1)
    pdf.cell(0, 8, f"Total Selling Price: ${total_selling:.2f}", ln=1)
    pdf.cell(0, 8, f"Total Revenue:       ${total_revenue:.2f}", ln=1)
    
    return pdf


# ----------------------------------
# STREAMLIT APP
# ----------------------------------
st.title("📈 Advanced Financial Tracker with PDF Reports")

tab1, tab2, tab3 = st.tabs(["Create New Sheet", "Add Entry", "View Data & Reports"])

# 1) CREATE NEW SHEET
with tab1:
    st.header("Create New Spreadsheet")
    new_sheet_name = st.text_input("Spreadsheet Name")
    user_email = st.text_input("Your Google Email for Access")
    
    if st.button("Create Sheet"):
        if new_sheet_name and user_email:
            new_spreadsheet = create_new_spreadsheet(new_sheet_name, user_email)
            if new_spreadsheet:
                st.success(f"✅ Spreadsheet '{new_sheet_name}' created!")
                st.markdown(f"**Access URL:** {new_spreadsheet.url}")
        else:
            st.warning("Please provide both a spreadsheet name and an email.")

# 2) ADD NEW ENTRY
with tab2:
    st.header("➕ Add New Transaction")
    
    spreadsheets = gc.openall()
    if spreadsheets:
        selected_sheet = st.selectbox("Select Spreadsheet", [sh.title for sh in spreadsheets])
        spreadsheet = gc.open(selected_sheet)
        
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Transaction Date")
            description = st.text_input("Description")
            buying_price = st.number_input("Buying Price ($)", min_value=0.0, format="%.2f")
        
        with col2:
            selling_price = st.number_input("Selling Price ($)", min_value=0.0, format="%.2f")
            revenue = selling_price - buying_price
            # Show computed revenue as read-only
            st.text_input("Calculated Revenue ($)", value=f"{revenue:.2f}", disabled=True)
            category = st.selectbox("Category", ["Inventory", "Services", "Products", "Other"])
        
        memo = st.text_area("Memo/Notes")
        
        if st.button("Add Transaction"):
            # Prepare entry for Google Sheet
            entry = [
                str(date),
                description,
                f"{buying_price:.2f}",
                f"{selling_price:.2f}",
                f"{revenue:.2f}",
                category,
                memo
            ]
            if add_entry_to_sheet(spreadsheet, entry):
                st.success("Transaction added successfully!")
                
                # -------------------
                # Immediately offer a PDF of this single transaction
                # -------------------
                pdf_single = generate_single_transaction_pdf(entry)
                pdf_buffer_single = BytesIO()
                pdf_single.output(pdf_buffer_single)
                pdf_buffer_single.seek(0)
                
                st.download_button(
                    label="🖨️ Print/Download This Transaction as PDF",
                    data=pdf_buffer_single,
                    file_name=f"transaction_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("No spreadsheets found. Please create one first!")


# 3) VIEW DATA & REPORTS
with tab3:
    st.header("📊 View Data & Generate Reports")
    
    spreadsheets = gc.openall()
    if spreadsheets:
        selected_sheet = st.selectbox("Select Spreadsheet", [sh.title for sh in spreadsheets], key="view")
        spreadsheet = gc.open(selected_sheet)
        
        df = get_sheet_data(spreadsheet)
        
        if not df.empty:
            try:
                # Convert 'Date' column to actual date
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                
                st.subheader("🔍 Filter Options")
                timeframe = st.selectbox("Timeframe", ["All", "Daily", "Monthly", "Yearly"])
                
                filtered_df = df.copy()
                selected_date = None
                month = None
                year = None
                
                if timeframe == "Daily":
                    selected_date = st.date_input("Select Date")
                    filtered_df = df[df['Date'] == selected_date]
                
                elif timeframe == "Monthly":
                    colm1, colm2 = st.columns(2)
                    with colm1:
                        month = st.selectbox(
                            "Month",
                            range(1, 13),
                            format_func=lambda x: datetime(1900, x, 1).strftime('%B')
                        )
                    with colm2:
                        year = st.number_input(
                            "Year",
                            min_value=2000,
                            max_value=2100,
                            value=datetime.now().year
                        )
                    filtered_df = df[
                        (df['Date'].apply(lambda x: x.month) == month) &
                        (df['Date'].apply(lambda x: x.year) == year)
                    ]
                
                elif timeframe == "Yearly":
                    year = st.number_input(
                        "Year",
                        min_value=2000,
                        max_value=2100,
                        value=datetime.now().year
                    )
                    filtered_df = df[df['Date'].apply(lambda x: x.year) == year]
                
                # Show filtered data
                st.subheader("📄 Transaction Records")
                st.dataframe(filtered_df, use_container_width=True)
                
                # Summary
                st.subheader("💰 Financial Summary")
                if not filtered_df.empty:
                    # We already converted these columns to numeric in get_sheet_data()
                    colA, colB, colC = st.columns(3)
                    
                    total_buying = filtered_df['Buying Price'].sum()
                    total_selling = filtered_df['Selling Price'].sum()
                    total_revenue = filtered_df['Revenue'].sum()
                    
                    with colA:
                        st.metric("Total Buying", f"${total_buying:.2f}")
                    with colB:
                        st.metric("Total Selling", f"${total_selling:.2f}")
                    with colC:
                        st.metric("Total Revenue", f"${total_revenue:.2f}")
                
                # PDF Report for the filtered data
                st.subheader("📤 Generate PDF Report for Filtered Data")
                if st.button("Generate Report"):
                    with st.spinner("Creating PDF..."):
                        pdf = generate_pdf_report(
                            filtered_df,
                            timeframe,
                            selected_date=selected_date,
                            month=month,
                            year=year
                        )
                        
                        pdf_buffer = BytesIO()
                        pdf.output(pdf_buffer)
                        pdf_buffer.seek(0)
                        
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_buffer,
                            file_name=f"financial_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            except KeyError:
                st.error("Invalid spreadsheet format. Please use sheets created by this app.")
        else:
            st.warning("No transactions found in the selected spreadsheet.")
    else:
        st.warning("No spreadsheets available. Please create one first!")

st.markdown("---")
st.markdown("_Built with Streamlit, Google Sheets, and FPDF_")
