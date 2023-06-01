# import pandas as pd
# import streamlit as st
# import geopandas as gpd
# import matplotlib.pyplot as plt
# from clean_dataframe import clean_dataframe
# import os


# def analyse_par_pays():
#     df_full = clean_dataframe()  # Define df_full within the function
#     shapefile_path = "ne_110m_admin_0_countries.shp"
#     os.environ["SHAPE_RESTORE_SHX"] = "YES"
#     country_data = gpd.read_file(shapefile_path)
#     st.title("Production countries")

#     # Get unique genre values
#     genre_values = df_full['genres_combined'].unique()
#     # Create a multiselect widget for genre filtering
#     selected_genres = st.multiselect(
#         'Select genres', genre_values, default=genre_values)

#     # Add a year slider
#     start_year, end_year = st.slider('Select a range of years', min_value=int(
#         df_full['year'].min()), max_value=int(df_full['year'].max()), value=(2010, 2022))

#     # Filter the data for the selected range of years and selected genres
#     filtered_data = df_full[df_full['year'].between(
#         start_year, end_year) & df_full['genres_combined'].isin(selected_genres)]

#     # Group the filtered data by production country and count the number of films
#     country_counts = filtered_data['production_countries'].value_counts()

#     # Read the country code data from the CSV file
#     country_codes_df = pd.read_csv(
#         'country_codesCR.csv', delimiter=',', quotechar='"')

#     # Create a new DataFrame with the country counts
#     country_counts_df = pd.DataFrame(
#         country_counts.index, columns=['ISO-3166\nalpha2'])
#     country_counts_df['Count'] = country_counts.values

#     # Merge country counts with country codes data
#     merged_data = pd.merge(country_data, country_counts_df,
#                            left_on='ADM0_A3', right_on='ISO-3166\nalpha2', how='left')

#     # Convert MultiPolygon geometries to Polygon geometries
#     merged_data['geometry'] = merged_data['geometry'].apply(
#         lambda geom: geom.geoms[0] if geom.geom_type == 'MultiPolygon' else geom)

#     # Plot the country boundaries and color them based on the film count
#     fig, ax = plt.subplots(figsize=(10, 8))
#     merged_data.plot(column='Count', cmap='Reds', linewidth=0.5, ax=ax, edgecolor='black', legend=True)
#     st.pyplot(fig)


# if __name__ == "__main__":
#     df_full = clean_dataframe()
#     analyse_par_pays()


import pandas as pd
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from clean_dataframe import clean_dataframe
import os

#  POWER BIIIIIIIIIIIII


def analyse_par_pays():
    st.markdown('<iframe title="my_movies" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=c02682a0-7d74-4561-b964-b84cc13084e4&autoAuth=true&ctid=5892e2db-e39d-4cc1-a179-dc66550efc30" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)


if __name__ == "__main__":
    df_full = clean_dataframe()
    analyse_par_pays()
