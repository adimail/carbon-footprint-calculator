import streamlit as st
from modules.pages import home_page
from modules.pages import model_page
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Carbon Footprint Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    with st.sidebar:
        page = option_menu(
            "Carbon footprint calculator", ["Home", "Model"],
            icons=["house-door-fill", "tools"],
            menu_icon="tree-fill",
            default_index=1
        )

    if page == "Home":
        home_page()
    elif page == "Model":
        model_page()


if __name__ == "__main__":
    main()