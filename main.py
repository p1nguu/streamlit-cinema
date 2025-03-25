## IMPORTS ##
import pandas as pd
import streamlit as st
import numpy as np

import matplotlib.pyplot as plt
from threading import RLock

## SETTINGS ##
matplotlib_active = False
show_genres = False

## LOAD FILE ##
filename = "movies.csv"
data = pd.read_csv(filename, sep=',')

## LOAD GENRES ##
genres = []
for rawGenre in data['genres']:
    for genre in rawGenre.split('|'):
        if genre not in genres:
            genres.append(genre)

## LOAD FILMS PER GENRE ##
filmsPerGenre = {}
for genre in genres:
    filmsPerGenre[genre] = []
for index, filmRow in data.iterrows():
    for genre in filmRow['genres'].split('|'):
        filmsPerGenre[genre].append(filmRow['title'])

st.write("""
# Le cinéma dans le monde
         """)

#st.write(data.head())
st.page_link('https://github.com/fragmadata/MovieDataset/tree/master', label="Source de ce travail (données)")
st.write("Nombre de films: ", len(data))
st.write("Nombre de genres: ", len(genres) - 1)
if show_genres:
    st.write("## Genres: ")
    for genre in genres[0:len(genres)-1]:
        st.write("""- """ + genre)


## PLOT GENRE HISTOGRAM (matplotlib)
if matplotlib_active:
    _lock = RLock()
    with _lock:
        fig, ax = plt.subplots()
        count = []
        for films in filmsPerGenre.values():
            count.append(len(films))
        ax.bar(filmsPerGenre.keys(), count)
        st.pyplot(fig)

## PLOT GENRE HISTOGRAM (streamlit)
filmsPerGenre_df = pd.DataFrame({
    'Genre': list(filmsPerGenre.keys()),
    'Nombre de films': [len(films) for films in filmsPerGenre.values()]
})
st.bar_chart(filmsPerGenre_df, x='Genre', y='Nombre de films')

## EXTRACT YEARS ##
import re

filmsPerYear = {}
for index, row in data.iterrows():
    match = re.search(r'\((\d{4})\)', row['title'])
    if match:
        year = match.group(1)
        if year not in filmsPerYear:
            filmsPerYear[year] = []
        filmsPerYear[year].append(row['title'])

## PLOT PER YEAR
filmsPerYear_df = pd.DataFrame({
    'Année': list(filmsPerYear.keys()),
    'Nombre de films': [len(films) for films in filmsPerYear.values()]
})
year = st.slider('Année', 1900, 2016, 2000)

st.write("## Films de l'année ", year)
if str(year) in filmsPerYear:
    st.write(filmsPerYear[str(year)])
else:
    st.write('Aucun film trouvé pour cette année')