from pages import info, settings, main
from multipage import MultiPage
import streamlit as st

app = MultiPage()

# Add all your application here
app.add_page("Home", "house", main.app)
app.add_page("Settings", "gear", settings.app)
app.add_page("Info", "info", info.app)

app.run()