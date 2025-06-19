import streamlit as st

import pandas as pd
import numpy as np

import pickle
import os
from pathlib import Path

st.write("""
## Boxing Machine Learning Predictions WebApp

This app predicts **boxing match** outcomes!  Predict wins, losses, and draws for your favorite boxers for upcoming matches!
         
For accuracy, please make sure to **only use the official boxing undercard for each fight**.
         
You may check upcoming undercards at https://box.live/fight-results/. 
         
""")

st.divider()

def user_input_features():

    fighter1_column, fighter2_column = st.columns(2)
    
    fighter1_column.markdown("### Fighter 1")
    fighter1_column.markdown("This data should be for the fighter on the **left** of the undercard.")
    fighter1_column.markdown("This is the **\"home\"** fighter, that is more favored to win.")

    fighter1_record_wins = fighter1_column.number_input("Fighter 1 Wins", 0, 100, value=30, step=1, key="fighter1wins")
    fighter1_record_draws = fighter1_column.number_input("Fighter 1 Draws", 0, 100, value=2, step=1, key="figher1draws")
    fighter1_record_losses = fighter1_column.number_input("Fighter 1 Losses", 0, 100, value=5, step=1, key="fighter1losses")
    fighter1_height_cm = fighter1_column.number_input("Fighter 1 Height (in cm)", 100., 250., value=180., step=0.1, key="fighter1height")
    fighter1_debut = fighter1_column.number_input("Fighter 1 Debut (year)", 1800, 2030, value=2021, step=1, key="fighter1debut_year")

    fighter2_column.markdown("### Fighter 2")
    fighter2_column.markdown("This data should be for the fighter on the **right** of the undercard.")
    fighter2_column.markdown("This is the **\"challenger\"** fighter, that is typically less favored to win.")

    fighter2_record_wins = fighter2_column.number_input("Fighter 2 Wins", 0, 100, value=20, step=1, key="fighter2wins")
    fighter2_record_draws = fighter2_column.number_input("Fighter 2 Draws", 0, 100, value=2, step=1, key="figher2draws")
    fighter2_record_losses = fighter2_column.number_input("Fighter 2 Losses", 0, 100, value=10, step=1, key="fighter2losses")
    fighter2_height_cm = fighter2_column.number_input("Fighter 2 Height (in cm)", 100., 250., value=180., step=0.1, key="fighter2height")
    fighter2_debut = fighter2_column.number_input("Fighter 2 Debut (year)", 1800, 2030, value=2018, step=1, key="fighter2debut_year")

    data = {"fighter1_record_wins": fighter1_record_wins,
            "fighter1_record_draws": fighter1_record_draws,
            "fighter1_record_losses": fighter1_record_losses,
            "fighter2_record_wins": fighter2_record_wins,
            "fighter2_record_draws": fighter2_record_draws,
            "fighter2_record_losses": fighter2_record_losses,
            "fighter1_height_cm": fighter1_height_cm,
            "fighter2_height_cm": fighter2_height_cm,
            "fighter1_debut": fighter1_debut,
            "fighter2_debut": fighter2_debut
            }
    
    data = pd.DataFrame(data, index=[0])

    return data


@st.cache_data
def read_data():

    # get current path of this file, set it to path
    curr_dir = os.getcwd()

    # csv file path
    my_file_path = Path(curr_dir + "/train-data/fight_data.csv")
    df_init = pd.read_csv(my_file_path).fillna(pd.NA).drop(columns=["fighter2_ko_percentage","fighter1_ko_percentage"])

    # backup csv file path
    backup_file_path = Path(curr_dir + "/train-data/fight_data_backup_basic.csv")
    df_init = pd.concat([df_init,pd.read_csv(backup_file_path)], axis=0)

    # clean a little
    df_init = df_init.drop_duplicates()
    df_essentials = df_init.drop(columns=['link','Venue','Date','Undercard fights','fighter1','fighter2'])
    df_staged_cleaning = df_essentials.copy()
    df_staged_cleaning['method_or_round'] = df_staged_cleaning['method_or_round'].str.split(' ')
    df_staged_cleaning = df_staged_cleaning.drop(columns='method_or_round')
    df_encoded = df_staged_cleaning.copy()
    # WINNER = 0, LOSER = 1, DRAW = 2

    def custom_encoder(value) :
        if value == 'Winner' :
            return 0
        elif value == 'Loser' :
            return 1
        else : return 2 # draw
    df_encoded['fighter1_result'] = df_encoded['fighter1_result'].apply(custom_encoder)

    df_encoded['fighter1_result'] = df_encoded['fighter1_result'].astype('category')

    df_encoded['fighter1_record_wins'] = df_encoded['fighter1_record_wins'].astype('Int64')
    df_encoded['fighter1_record_draws'] = df_encoded['fighter1_record_draws'].astype('Int64')
    df_encoded['fighter1_record_losses'] = df_encoded['fighter1_record_losses'].astype('Int64')
    df_encoded['fighter2_record_wins'] = df_encoded['fighter2_record_wins'].astype('Int64')
    df_encoded['fighter2_record_draws'] = df_encoded['fighter2_record_draws'].astype('Int64')
    df_encoded['fighter2_record_losses'] = df_encoded['fighter1_record_losses'].astype('Int64')
    df_encoded['fighter1_height_cm'] = df_encoded['fighter2_height_cm'].astype('Int64')
    df_encoded['fighter2_height_cm'] = df_encoded['fighter2_height_cm'].astype('Int64')
    df_encoded['fighter1_debut'] = df_encoded['fighter1_debut'].astype('Int64')
    df_encoded['fighter2_debut'] = df_encoded['fighter1_debut'].astype('Int64')

    X = df_encoded.drop(columns=['fighter1_result'])

    return X


# load model and data, and input data
df_loaded = read_data()

input_df_pred_1 = user_input_features()
df_pred1 = pd.concat([input_df_pred_1, df_loaded], axis=0)
df_pred1 = df_pred1[:1].copy()



# swap and make prediction 2
df_staged_swapping = input_df_pred_1.copy()

fighter2_wins_temp = df_staged_swapping['fighter2_record_wins'].copy()
fighter2_draws_temp = df_staged_swapping['fighter2_record_draws'].copy()
fighter2_losses_temp = df_staged_swapping['fighter2_record_losses'].copy()
fighter2_height_cm_temp = df_staged_swapping['fighter2_height_cm'].copy()
fighter2_debut_temp = df_staged_swapping['fighter2_debut'].copy()

df_staged_swapping['fighter2_record_wins'] = df_staged_swapping['fighter1_record_wins']
df_staged_swapping['fighter2_record_draws'] = df_staged_swapping['fighter1_record_draws']
df_staged_swapping['fighter2_record_losses'] = df_staged_swapping['fighter1_record_losses']
df_staged_swapping['fighter2_height_cm'] = df_staged_swapping['fighter1_height_cm']
df_staged_swapping['fighter2_debut'] = df_staged_swapping['fighter1_debut']

df_staged_swapping['fighter1_record_wins'] = fighter2_wins_temp
df_staged_swapping['fighter1_record_draws'] = fighter2_draws_temp
df_staged_swapping['fighter1_record_losses'] = fighter2_losses_temp
df_staged_swapping['fighter1_height_cm'] = fighter2_height_cm_temp
df_staged_swapping['fighter1_debut'] = fighter2_debut_temp

df_pred2 = df_staged_swapping[:1].copy()

curr_dir = os.getcwd()
xgbc_path = curr_dir + '/models/basic_xgboost.pkl'
load_xgbc = pickle.load(open(xgbc_path, 'rb'))


# calculate predictions
prediction1_probas = load_xgbc.predict_proba(df_pred1)
prediction = np.argmax(prediction1_probas)


# make predict button
pred_button = st.button("Predict", type="primary")


if pred_button:
    # DISPLAY PRED
    # prediction is the label index, so use indexing to choose the correct species
    st.markdown('## Prediction')

    fighter1_outcomes = np.array(['Win🏆', 'Loss ❌', 'Draw 🟰'])
    st.markdown(f"### Fighter 1 **{fighter1_outcomes[prediction]}**")

    fighter2_outcomes = np.array(['Loss ❌', 'Win 🏆', 'Draw 🟰'])
    st.markdown(f"### Fighter 2 **{fighter2_outcomes[prediction]}**")


    st.subheader('Prediction probability for fighter 1:')
    prediction_probas = pd.DataFrame(prediction1_probas, columns=["Win 🏆", "Loss ❌", "Draw 🟰"])
    st.write(prediction_probas)

    st.subheader('Prediction probability for fighter 1:')
    prediction_probas = pd.DataFrame(prediction1_probas, columns=["Loss ❌", "Win 🏆", "Draw 🟰"])
    st.write(prediction_probas)
