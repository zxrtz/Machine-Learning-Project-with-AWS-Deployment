import streamlit as st

import pandas as pd
import numpy as np

import pickle
import joblib

st.write("""
# Boxing Predictions App

This app predicts **boxing match** outcomes! 
         
Predict wins, losses, and draws for your favorite boxers against any opponent!
         
Data is web scraped and trained off of https://box.live/fight-results/.
""")

st.divider()

def user_input_features():

    fighter1_column, fighter2_column = st.columns(2)
    
    fighter1_record_wins = fighter1_column.number_input("Fighter 1 Wins", 0, 100, value=20, step=1, key="fighter1wins")
    fighter1_record_draws = fighter1_column.number_input("Fighter 1 Draws", 0, 100, value=15, step=1, key="figher1draws")
    fighter1_record_losses = fighter1_column.number_input("Fighter 1 Losses", 0, 100, value=10, step=1, key="fighter1losses")
    fighter1_height_cm = fighter1_column.number_input("Fighter 1 Height (in cm)", 100., 250., value=180., step=0.1, key="fighter1height")
    fighter1_debut = fighter1_column.number_input("Fighter 1 Debut (year)", 1800, 2030, value=2025, step=1, key="fighter1debut_year")

    fighter2_record_wins = fighter2_column.number_input("Fighter 2 Wins", 0, 100, value=20, step=1, key="fighter2wins")
    fighter2_record_wins = fighter2_column.number_input("Fighter 2 Draws", 0, 100, value=5, step=1, key="figher2draws")
    fighter2_record_wins = fighter2_column.number_input("Fighter 2 Losses", 0, 100, value=10, step=1, key="fighter2losses")
    fighter2_height_cm = fighter2_column.number_input("Fighter 2 Height (in cm)", 100., 250., value=180., step=0.1, key="fighter2height")
    fighter2_debut = fighter2_column.number_input("Fighter 2 Debut (year)", 1800, 2030, value=2025, step=1, key="fighter2debut_year")

    data = {"fighter1_record_wins": fighter1_record_wins,
            "fighter1_record_draws": fighter1_record_draws,
            "fighter1_record_losses": fighter1_record_losses,
            "fighter2_record_wins": fighter2_record_wins,
            "fighter2_record_draws": fighter2_record_wins,
            "fighter2_record_losses": fighter2_record_wins,
            "fighter1_height_cm": fighter1_height_cm,
            "fighter2_height_cm": fighter2_height_cm,
            "fighter1_debut": fighter1_debut,
            "fighter2_debut": fighter2_debut
            }

    return pd.DataFrame(data, index=[0])


@st.cache_data
def read_data():
    df_init = pd.read_csv("data/fight_data.csv").fillna(pd.NA)
    df_init = pd.concat([df_init,pd.read_csv("data/fight_data_backup_basic.csv")], axis=0)
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
    df_encoded['fighter1_ko_percentage'] = df_encoded['fighter1_ko_percentage'].astype('Int64')
    df_encoded['fighter2_ko_percentage'] = df_encoded['fighter2_ko_percentage'].astype('Int64')
    df_encoded['fighter1_debut'] = df_encoded['fighter1_debut'].astype('Int64')
    df_encoded['fighter2_debut'] = df_encoded['fighter1_debut'].astype('Int64')

    X = df_encoded.drop(columns=['fighter1_result', "fighter1_ko_percentage", 'fighter2_ko_percentage'])

    return X


# load model and data
input_df = user_input_features()
df_loaded = read_data()

df = pd.concat([input_df, df_loaded], axis=0)
df = df[:1]

load_xgbc = pickle.load(open('models/basic_xgboost.pkl', 'rb'))


# make predict button
st.button("Predict", type="primary")


# calculate predictions
st.write("""## Your Prediction:""")
prediction = load_xgbc.predict(df)
prediction_probas = load_xgbc.predict_proba(df)


# DISPLAY PRED
# prediction is the label index, so use indexing to choose the correct species
st.subheader('Prediction')
outcomes = np.array(['Win', 'Loss', 'Draw'])
st.write(outcomes[prediction])

st.subheader('Prediction probability for each outcome:')
prediction_probas = pd.DataFrame(prediction_probas, columns=["Win", "Loss", "Draw"])
st.write(prediction_probas)
