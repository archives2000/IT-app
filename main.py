import streamlit as st
from dashboard import dashboard
from framework import framework

pages = {
    "Navigation": [
        st.Page(dashboard, title="Dashboard"),
        st.Page(framework, title="Framework"),
    ]
}

pg = st.navigation(pages, position="top")
pg.run()
