import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium as fol
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium
sns.set(style='dark')

#Function
def sort_by_station(df):
    res_df = df.groupby('station')
    return res_df
def sort_by_pollutants(df,pollutants):
    res_df = df.groupby('station')[pollutants].mean()
    return res_df
def plot_monthly_trend(df,pollutant,year = ""):
    month_label = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sept','Okt','Nov','Des']
    plt.figure(figsize=(8,4))
    if year:
        year=year
        sns.lineplot(x='month', y=pollutant, data=df, marker='o')
    else:
        year = "2013-2017"
        sns.lineplot(x='month', y=pollutant, hue='year', data=df, marker='o', palette='viridis')
        plt.legend(title='tahun', bbox_to_anchor=(1,1), loc='upper right')

    plt.title(f'Tren Bulanan {pollutant} {year}')
    plt.xlabel('Bulan')
    plt.ylabel(f'{pollutant} \u03BCg/m\u00B3')
    plt.xticks(range(1,13), month_label)
    plt.grid(True)
    plt.tight_layout()
    return plt

#Load dataset
all_df = pd.read_csv("./Datasets/all_data.csv")
loc_df = pd.read_csv("./Datasets/stasiun_koordinat.csv")
all_df.sort_values(by="datetime", inplace=True)
pollutants = ['PM2.5','PM10','SO2','NO2','CO','O3']
env_vars = ['TEMP','PRES','DEWP','RAIN','WSPM']
col_interest = pollutants+env_vars

#Filter data
min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()
station_df = sort_by_station(all_df)

st.header('Dashboard Monitoring Kualitas Udara Tiongkok')

st.divider()
st.subheader('Peringkat Rata-rata polusi setiap lokasi')
start_date,end_date = st.date_input(
    label = "Piih Periode Data",
    value = [min_date,max_date],
    min_value = min_date,
    max_value = max_date
)


main_df = all_df[(all_df["datetime"] >= str(start_date)) & (all_df["datetime"] <= str(end_date))]

#Filtered Frame
rank_df = sort_by_pollutants(main_df,pollutants)
monthly_df = all_df.groupby(['year','month'])[pollutants].mean().reset_index()

pollutant_list = st.selectbox(
        label="Pilih jenis polutan",
        options = pollutants
        )

df_sorted = rank_df.sort_values(by=pollutant_list, ascending=False)

col1,col2 = st.columns(2)
with col1:
    highest_stat = df_sorted.index[0]
    highest_val = df_sorted[pollutant_list][0]
    st.metric(f'Tertinggi ({highest_stat})',f'{highest_val:.3f} \u03BCg/m\u00B3')
with col2:
    n = len(df_sorted)-1
    lowest_stat = df_sorted.index[n]
    lowest_val = df_sorted[pollutant_list][n]
    st.metric(f'Terendah ({lowest_stat})', f'{lowest_val:.3f} \u03BCg/m\u00B3')

fig,ax = plt.subplots(figsize=(20,10))
sns.barplot(x=df_sorted[pollutant_list],y=df_sorted.index, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(f'rata-rata {pollutant_list}(\u03BCg/m\u00B3)', fontsize=18)
ax.set_title(f'Rangking Polutan {pollutant_list}', loc="center", fontsize=20)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)

st.pyplot(fig)

st.divider()
st.subheader("Tren Rerata Polusi Bulanan")

years = st.selectbox ( 
    label="Pilih Tahun",
    options = all_df.groupby("year")
)

tren_df = monthly_df[monthly_df['year'] == years]

all_years = st.checkbox("Lihat Semua Tahun")

for i in pollutants:
    if all_years:
        chart = plot_monthly_trend(monthly_df,i)
    else:
        chart = plot_monthly_trend(tren_df,i,years)
    st.pyplot(plt)

st.divider()
st.subheader("Korelasi Kondisi Lingkungan dengan Polutan Udara")

correlation_df = all_df[col_interest]
correlation_matrix = correlation_df.corr()
corr_chart = plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidth=0.5)
plt.title("Diagram Korelasi")
st.pyplot(corr_chart)

st.divider()
st.subheader("Analisis Geospasial")
st.write("Peta sebaran lokasi pengamatan dan tingkat polusinya")

pollutants_map = st.selectbox(
        label="Pilih polutan",
        options = pollutants
        )

map_data_df = all_df.groupby(['longitude','latitude','station'])[pollutants_map].mean().reset_index() 
heat_data = [[row['latitude'],row['longitude'],row[pollutants_map]] for _, row in map_data_df.iterrows()]

m = fol.Map(location=[35.8617,104.1954], zoom_start=5)
HeatMap(heat_data).add_to(m)
for _, row in loc_df.iterrows():
    fol.Marker(
            location=[row['latitude'],row['longitude']],
            popup=row['station'],
            icon=fol.Icon(color='red', icon='info-sign')
            ).add_to(m)

st_folium(m, width=700, height=500)


