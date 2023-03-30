import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64

df = pd.read_csv('concat_client_collect.csv')

# Création du titre de la page :
st.title("Visualisation des dépenses par catégorie en fonction de la catégorie socioprofessionnelle")

# Sélection de la catégorie socioprofessionnelle :
career_selected = st.selectbox('Sélectionnez une catégorie socioprofessionnelle', df['career'], key='select1')

# Filtre des données pour n'afficher que la catégorie socioprofessionnelle sélectionnée :
filtered_df = df[df['career'] == career_selected]

# Création Graphique :
melted_df = pd.melt(filtered_df, id_vars=['career'], value_vars=['cloths', 'underwear', 'sportswear', 'accessories'], var_name='Catégorie', value_name='Dépenses')
chart = alt.Chart(melted_df).mark_bar().encode(
    x='Catégorie',
    y='Dépenses',
    color='Catégorie'
).properties(
    title='Dépenses par catégorie pour la catégorie socioprofessionnelle : {}'.format(career_selected),
    width=alt.Step(80)
)

st.altair_chart(chart, use_container_width=True)


#-------------------------------------------------
# Affichage de la sélection de catégorie socioprofessionnelle
career_selected2 = st.selectbox('Sélectionnez une catégorie socioprofessionnelle', df['career'], key='select2')

# Filtre du DataFrame en fonction de la catégorie sélectionnée
df_filtered2 = df[df['career'] == career_selected2]

# Calcul de la dépense moyenne du panier pour la catégorie sélectionnée
mean_spending = df_filtered2['shopping_price'].mean()

# Création du graphique
chart2 = alt.Chart(df_filtered2).mark_bar().encode(
    x=alt.X('career', title='Métier'),
    y=alt.Y('shopping_price', title='Total Des Paniers'),
    tooltip=[alt.Tooltip('shopping_price', title='Dépense moyenne')],
).properties(
    title=f'Dépense moyenne du panier pour la catégorie "{career_selected2}" : {mean_spending:.2f} €'
)

# Affichage du graphique
st.altair_chart(chart2, use_container_width=True)


# Affichage de la saisie utilisateur pour le nombre de lignes à exporter
nrows = st.number_input('Nombre de lignes à exporter', min_value=1, value=50, step=1)

# Créer un sous-ensemble de données à exporter
subset_data = df.iloc[:, 4:]

# Fonction pour exporter les données
def download_csv(data):
    csv_file = subset_data.head(nrows).to_csv(index=False, sep=';')
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="collect_data.csv">Télécharger les données CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

# Créer un bouton pour télécharger les données CSV
if st.button('Télécharger les données CSV'):
    download_csv(subset_data)