import streamlit as st
from netfilms_p2 import page_2
from netfilms_p3 import page_3
from netfilms_home import page_home
from clean_dataframe import clean_dataframe
from netfilms_analyse_par_pays import analyse_par_pays
from netfilms_analyse import analyse
# Set the default layout to wide mode
st.set_page_config(layout="wide")


def main():

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", ("Home", "Analyse des KPI", "Analyse par période"))
    # "Go to", ("Home", "Analyse des KPI", "Analyse par genre", "Analyse par période", "Analyse"))

    # Load the cleaned dataframe
    df_full = clean_dataframe()

    if page == "Home":
        page_home()

    elif page == "Analyse par genre":
        page_3(df_full)

    elif page == "Analyse par période":
        page_2(df_full)

    elif page == "Analyse":
        analyse(df_full)

    elif page == "Analyse des KPI":
        analyse_par_pays()


if __name__ == "__main__":
    main()
