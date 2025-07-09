import pandas as pd
import streamlit as st
import io

# Sidebar
page = st.sidebar.selectbox("Navigation", ["Dashboard", "Monitor Inventory", "HAM"])

def dashboard():
    st.title("Dashboard")

def monitor_inventory_page():

    excel_file = "monitor_inventory.xlsx"
    excel_sheet_name  = "DATA"

    if 'data' not in st.session_state:
        st.session_state['data'] = []

    st.title("Monitor Inventory")
    desk_number = st.text_input("Desk Number")
    monitor_type = st.selectbox("Monitor Type", ["", "Current Monitors", "Past Monitors"], format_func=lambda x: x if x else "Select Monitor Type")
    if monitor_type:
        with st.form(key='entry_form', clear_on_submit=True):
            serial_number1 = st.text_input("Serial Number 1")
            serial_number2 = st.text_input("Serial Number 2")
            status = st.selectbox("Status", ["Updated", "Replace Full", "Replace One", "Replace Stock"])
            comments = st.text_input("Comments")
            submitted = st.form_submit_button("Add Entry")

            # Collect Data if every box is filled
            if submitted and serial_number1 and serial_number2 and desk_number:
                st.session_state['data'].append({
                    'Desk Number': desk_number,
                    'Monitor Type': monitor_type,
                    'Serial 1': serial_number1,
                    'Serial 2': serial_number2,
                    'Status': status
                })
                st.success("Entry added!")
    else:
        st.info("Please select a monitor type.")

    # Show current table
    if st.session_state['data']:
        df = pd.DataFrame(st.session_state['data'])
        st.dataframe(df, use_container_width=True)

        # Save to Excel 
        if st.button("Save to Excel"):
            out_df = pd.DataFrame(st.session_state['data'])
            out_df.to_excel(excel_file, sheet_name=excel_sheet_name, index=False)
            st.success(f"Data written to `{excel_file}`")

            # Download directly
            buffer = io.BytesIO()
            out_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="Download Updated Excel",
                data= buffer,
                file_name="updated_inventory.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def HAM():

    excel_file = "HAM-CHLA.xlsx"
    excel_sheet_name  = "Template"

    if 'ham_data' not in st.session_state:
        st.session_state['ham_data'] = []

    st.title("HAM")

    # Import Excel
    uploaded_file = st.file_uploader("Import existing Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df_import = pd.read_excel(uploaded_file)
        st.session_state['ham_data'] = df_import.to_dict(orient='records')

    # Default settings for each model category
    manufacturer_defaults = {
        "monitor": "HP",
        "pc": "HP",
        "iphone": "Apple"
    }

    monitor_type = st.selectbox("Model Category", ["", "Monitor", "PC", "IPhone"], format_func=lambda x: x if x else "Select Model Category")
    if monitor_type:
        with st.form(key='entry_form', clear_on_submit=True):
            serial_number = st.text_input("Serial Number")
            model = st.text_input("Model")
            default_manufacturer = manufacturer_defaults.get(monitor_type.lower(), "HP")
            manufacturer = st.text_input("Manufacturer", value=default_manufacturer)
            state = st.selectbox("State", ["In Stock", "Replace Full", "Replace One", "Replace Stock"])
            stockroom = st.text_input("Stockroom", value="CHLA StockRoom")
            support_group = st.text_input("Support group", value="OSS CH Lausanne")
            purchase_date = st.date_input("Purchase date")
            comments = st.text_input("Comments")
            submitted = st.form_submit_button("Add Entry")

            # Collect Data if every box is filled
            if submitted and serial_number and model and state and stockroom and support_group and purchase_date:

                # Duplicates
                if serial_number in [row['Serial Number'] for row in st.session_state['ham_data']]:
                    st.warning("Serial Number already exists !")
                else:
                    st.session_state['ham_data'].append({
                        'Serial Number': serial_number,
                        'Monitor Type': monitor_type,
                        'State': state,
                        'Model': model, 
                        'Manufacturer': manufacturer,
                        'State': state,
                        'Stockroom': stockroom,
                        'Support Groupo' : support_group,
                        'Purchase date': purchase_date.strftime("%Y-%m-%d"),
                        'Comments': comments
                    })
                    st.success("Entry added!")
    else:
        st.info("Please select a model category.")

    cols = st.columns(3)

    # Show current table
    if st.session_state['ham_data']:
        df = pd.DataFrame(st.session_state['ham_data'])
        st.dataframe(df, use_container_width=True)

        # Save to Excel 
        if cols[0].button("Save to Excel"):
            out_df = pd.DataFrame(st.session_state['ham_data'])
            out_df.to_excel(excel_file, sheet_name=excel_sheet_name, index=False)
            st.success(f"Data written to `{excel_file}`")

            # Download directly
            buffer = io.BytesIO()
            out_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="Download Updated Excel",
                data= buffer,
                file_name="HAM-CHLA.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Delete 
        if cols[2].button("Delete Last Row", type="primary"):
            st.session_state['ham_data'].pop()
            st.rerun()

# Navigation Logic
if page == "Dashboard":
    dashboard()
elif page == "Monitor Inventory":
    monitor_inventory_page()
elif page == "HAM":
    HAM()
