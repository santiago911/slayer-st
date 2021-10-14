import streamlit as st
import pandas as pd

import mfunc
import constants
import text

# streamlit page config
st.set_page_config(page_title="Slayer Streamlit", layout="wide")
# language
la = 0
t_language = ("简体中文","English")

#----------------------------------------#
# Title
r0c1, r0c2 = st.columns([6, 8])
# language selector
language = st.radio("请选择您的偏好语言 Please Select Your Language",t_language)

if language == "简体中文":
    la = 0
elif language == "English":
    la = 1

with r0c1:
    f"# {text.script_name[la]}"
    f"### {text.script_author[la]}"
with r0c2:
    st.image("buyme.png",caption=text.buyme[la],width=100)
    
    
#----------------------------------------#
# Arbitrage
with st.expander(text.text_arbit_0[la], expanded=True):
    r1c1, r1c2, r1c3, r1c4 = st.columns([6, 6, 6, 6])
    with r1c1:
        arbit_platforms_selection = st.multiselect(
            text.text_arbit_1_0[la], text.text_arbit_1_1[la], text.text_arbit_1_2[la], help = text.text_arbit_1_help[la])
    with r1c2:
        arbit_rebate_rate_required = st.slider(text.text_arbit_2_0[la], 190, 200, 196, help = text.text_arbit_2_help[la])
    with r1c3:
        arbit_stakes = st.text_input(text.text_arbit_3_0[la], "10000", help = text.text_arbit_3_help[la])
    with r1c4:
        arbit_time_limit = st.text_input(text.text_arbit_4_0[la], "48", help = text.text_arbit_4_help[la])

    r2c1, r2c2, r2c3 = st.columns([6, 6, 12])
    r3c1, r3c2, r3c3 = st.columns([4, 16, 4])
    with r2c1:
        arbit_primary_handicap_only = st.radio(text.text_arbit_5_0[la], text.text_arbit_5_1[la], help = text.text_arbit_5_help[la])
    with r2c2:
        arbit_table_show_type = st.radio(text.text_arbit_6_0[la], ("DataFrame", "Markdown Table"), help = text.text_arbit_6_help[la])
    with r2c3:
        ""
        ""
        if st.button(text.text_submit[la]):
            arbit_result_list = mfunc.ArbitSearch(
                platforms_selection = arbit_platforms_selection,
                time_limit = arbit_time_limit,
                primary_handicap_only = arbit_primary_handicap_only,
                rebate_rate_required = arbit_rebate_rate_required,
                stakes = arbit_stakes,
                language=la)
            if arbit_table_show_type == "DataFrame":
                arbit_match_data = pd.DataFrame(arbit_result_list, columns = text.text_arbit_df_columns[la])
                r3c2.write(arbit_match_data)
            elif arbit_table_show_type == "Markdown Table":
                arbit_match_data_mdtable = f"""
                {text.text_arbit_mdtable[la]}
                |---|---|---|---|---|---|---|---|---|---|---|
                """
                for game in arbit_result_list:
                    arbit_match_data_mdtable += f"| {game[0]}| {game[1]}|{game[2]}|{game[3]}|{game[4]}|{game[5]}|{game[6]}|{game[7]}|{game[8]}|{game[9]}|{game[10]}|" + "\n"
                r3c2.markdown(arbit_match_data_mdtable)
        
    