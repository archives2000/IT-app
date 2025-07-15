import streamlit as st
import pandas as pd
import io

def dual_monitors():

    excel_file = "monitors_inventory.xlsx"
    excel_sheet_name  = "Template"

    if 'monitors_data' not in st.session_state:
        st.session_state['monitors_data'] = []

    st.title("Monitors Inventory")

    # Import Excel
    uploaded_file = st.file_uploader("Import existing Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df_import = pd.read_excel(uploaded_file)
        st.session_state['monitors_data'] = df_import.to_dict(orient='records')
    
    with st.form(key='entry_form', clear_on_submit=False):
        serial_number1 = st.text_input("Serial Number 1")
        serial_number2 = st.text_input("Serial Number 2")
        model = st.text_input("Model", key="model")
        manufacturer = st.text_input("Manufacturer", value= "HP")
        state = st.selectbox("State", ["In Stock", "Replace Full", "Replace One", "Replace Stock"])
        stockroom = st.text_input("Stockroom", value="CHLA StockRoom")
        support_group = st.text_input("Support group", value="OSS CH Lausanne")
        purchase_date = st.date_input("Purchase date")
        comments = st.text_input("Comments")
        submitted = st.form_submit_button("Add Entry")

        if submitted and serial_number1 and serial_number2 and model and state and stockroom and support_group and purchase_date:
            if serial_number1 in [row['Serial Number 1'] for row in st.session_state['monitors_data']]:
                st.warning("Serial Number already exists !")
            else:
                st.session_state['monitors_data'].append({
                    'Serial Number 1': serial_number1,
                    'Serial Number 2': serial_number2,                        
                    'State': state,
                    'Model': model, 
                    'Manufacturer': manufacturer,
                    'Stockroom': stockroom,
                    'Support Group' : support_group,
                    'Purchase date': purchase_date.strftime("%Y-%m-%d"),                        'Comments': comments
                    })
                st.success("Entry added!")
                st.rerun()


    cols = st.columns(3)

    # Show current table
    if st.session_state['monitors_data']:
        df = pd.DataFrame(st.session_state['monitors_data'])
        st.dataframe(df, use_container_width=True)

        # Save to Excel 
        if cols[0].button("Save to Excel"):
            out_df = pd.DataFrame(st.session_state['monitors_data'])
            out_df.to_excel(excel_file, sheet_name=excel_sheet_name, index=False)
            st.success(f"Data written to `{excel_file}`")

            # Download directly
            buffer = io.BytesIO()
            out_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="Download Updated Excel",
                data= buffer,
                file_name="monitors_inventory.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Delete 
        if cols[2].button("Delete Last Row", type="primary"):
            st.session_state['monitors_data'].pop()
            st.rerun()