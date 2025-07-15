import streamlit as st
import pandas as pd
import io

def ham():

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
    
    monitor_type = st.selectbox("Model Category", ["", "Monitor", "PC", "IPhone"],
                            format_func=lambda x: x if x else "Select Model Category",
                            key="monitor_type")
    if monitor_type:

        with st.form(key='entry_form', clear_on_submit=True):
            serial_number = st.text_input("Serial Number")
            model = st.text_input("Model", key="model", value="HP EliteBook 850 G8")
            default_manufacturer = manufacturer_defaults.get(monitor_type.lower(), "HP")
            manufacturer = st.text_input("Manufacturer", value=default_manufacturer)
            state = st.selectbox("State", ["In Stock", "Replace Full", "Replace One", "Replace Stock"])
            stockroom = st.text_input("Stockroom", value="CHLA StockRoom")
            support_group = st.text_input("Support group", value="OSS CH Lausanne")
            purchase_date = st.date_input("Purchase date")
            comments = st.text_input("Comments")
            submitted = st.form_submit_button("Add Entry")

            if submitted and serial_number and model and state and stockroom and support_group and purchase_date:
                if serial_number in [row['Serial Number'] for row in st.session_state['ham_data']]:
                    st.warning("Serial Number already exists !")
                else:
                    st.session_state['ham_data'].append({
                        'Serial Number': serial_number,
                        'Monitor Type': monitor_type,
                        'State': state,
                        'Model': model, 
                        'Manufacturer': manufacturer,
                        'Stockroom': stockroom,
                        'Support Group' : support_group,
                        'Purchase date': purchase_date.strftime("%Y-%m-%d"),
                        'Comments': comments
                    })
                    st.success("Entry added!")
                    st.rerun()

    else:
        st.info("Please select a model category.")

    cols = st.columns(3)

    # Show current table
    if st.session_state['ham_data']:
        df = pd.DataFrame(st.session_state['ham_data'])
        st.dataframe(df, use_container_width=True)

        if cols[0].button("Save to Excel"):
            if not st.session_state['ham_data']:
                st.warning("No data to save.")
            else:
                all_data = pd.DataFrame(st.session_state['ham_data'])

                # --- Write to disk AND (later) to a BytesIO buffer ---
                def write_multisheet(writer):
                    for category in ["Monitor", "PC", "IPhone"]:
                        filtered = all_data[all_data["Monitor Type"] == category]
                        if not filtered.empty:
                            filtered.to_excel(
                                writer,
                                sheet_name=category,
                                index=False
                            )

                # 1  save to disk
                try:
                    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as w:
                        write_multisheet(w)
                    st.success(f"Data saved to `{excel_file}` with per-category sheets.")
                except Exception as e:
                    st.error(f"Error saving Excel file: {e}")

                # 2  build download file with the same sheets
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl", mode="w") as w:
                    write_multisheet(w)
                buffer.seek(0)

                st.download_button(
                    "Download Updated Excel",
                    data=buffer,
                    file_name="HAM-CHLA.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        if cols[1].button("Clear Current Entry", type="secondary"):
            for key in ["model", "Serial Number", "Manufacturer", "Stockroom", "Support group", "Purchase date", "Comments"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.pop('monitor_type', None)
            st.rerun()

        # Delete 
        if cols[2].button("Delete Last Row", type="primary"):
            st.session_state['ham_data'].pop()
            st.rerun()
