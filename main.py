import streamlit as st
from dashboard import dashboard
from ham import ham
from iphone import iphone
from laptop import laptop
from login import login
from dual_monitors import dual_monitors

pages = {
    "Dashboard": [
        st.Page(dashboard, title="Dashboard"),
    ],
    "Templates": [
        st.Page(ham, title="HAM"),
        st.Page(dual_monitors, title="Monitors Inventory"),
    ],
     "Quick Fixes": [
        st.Page(iphone, title="iPhone"),
        st.Page(laptop, title="Laptop"),
        st.Page(login, title="Login"),
    ]
}

pg = st.navigation(pages, position="top")
pg.run()
