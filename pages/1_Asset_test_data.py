

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# existing data
data_url = "https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final3.csv"
df_fin = pd.read_csv(data_url)  
df_final = df_fin[df_fin["Platform type"] == "Well head"]

# new data
reserves_url = "https://raw.githubusercontent.com/PrateekKumar2109/Assset-production-monitoring/main/Data/updated_dataframe.csv"
df_reserves = pd.read_csv(reserves_url)

# filter df_reserves
df_reserves = df_reserves[(df_reserves['Status'] == 'Producing') & (df_reserves['Category'] == '2P')]

# mapping of area names to coordinates
area_coords = {
    'B134': {'lat': 18.73, 'long': 72.295},
    'B173A': {'lat': 18.68, 'long': 72.31},
    'Heera': {'lat': 18.47, 'long': 72.24},
    'Neelam': {'lat': 18.68, 'long': 72.26},
    'NW B173A': {'lat': 18.92, 'long': 72.26},
    'Ratna and R-Series': {'lat': 18.28, 'long': 72.25},
}


st.set_page_config(layout="wide") 

def map_plot(df, texts, font_size, show_lines=False):
    fig, ax = plt.subplots(figsize=(20, 16),dpi=600)  
    ax.set_facecolor('#e6f3ff') 

    sns.scatterplot(data=df, x='Longitude', y='Latitude', hue='Field', ax=ax, s=60)

    for i in range(len(df)):
        row = df.iloc[i]
        if texts:
            text = f"{row['Platform']}\n" + "\n".join([f"{text}: {row[text]}" for text in texts])
            text_color = 'orange' if row['Rig'] == 'yes' else 'black'
            ax.text(row['Longitude'], row['Latitude'], text, va='bottom', ha='left', fontsize=font_size, color=text_color,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
        else:
            ax.text(row['Longitude'], row['Latitude'], f"{row['Platform']}", va='bottom', ha='left', fontsize=16,
                    color='green' if row['Rig'] == 'yes' else 'black')

    if show_lines:
        lines = [
            {"start_lat": 18.72, "start_lon": 72.315, "length": 0.04, "angle": 30, "texts": [("Sector-I", 'bottom', 'left')]},
            {"start_lat": 18.77, "start_lon": 72.29, "length": 0.05, "angle": -13, "texts": [("Sector-II", 'top', 'left'), ("Sector-III", 'bottom', 'left')]},
            {"start_lat": 18.50, "start_lon": 72.24, "length": 0.04, "angle": 12, "texts": [("South Heera", 'bottom', 'left')]},
            {"start_lat": 18.609, "start_lon": 72.259, "length": 0.06, "angle": 145, "texts": [("Mid Heera", 'top', 'right'), ("North Heera", 'bottom', 'right')]}
        ]

        for line in lines:
            angle_rad = np.deg2rad(line["angle"])
            end_lat = line["start_lat"] + line["length"] * np.sin(angle_rad)
            end_lon = line["start_lon"] + line["length"] * np.cos(angle_rad)
            plt.plot([line["start_lon"], end_lon], [line["start_lat"], end_lat], linestyle='dashed', color='black')
            
            for text, va, ha in line['texts']:
                
                text_x, text_y = (end_lon, end_lat) if line is lines[3] else (line["start_lon"], line["start_lat"])
                text_x -= 0.015  # Shift text_x by -0.1
                text_y -= 0.015  # Shift text_y by -0.1
                ax.text(text_x, text_y, text, va=va, ha=ha, fontsize=font_size,
                        color='red', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.title('Offshore Platforms', fontsize=24)  
    plt.gca().axes.get_xaxis().set_visible(False)  
    plt.gca().axes.get_yaxis().set_visible(False) 

    return fig

st.title('NH Asset Platforms')

option = st.sidebar.selectbox('Select Option', ('None', 'OP', 'GP', 'WI', 'GI'), index=0)

show_lines = False
if option == 'None':
    texts = []
    font_size = 16
    show_lines = True
    # new plot
    selected_columns = ['Oil Inplace', 'Oil Ultimate', 'Oil Production', 'Oil Balance Reserves']
    for area in df_reserves['area'].unique():
        if area in area_coords:
            df_area = df_reserves[df_reserves['area'] == area]
            for column in selected_columns:
                value = df_area[column].sum()  # or any other aggregation you need
                plt.text(area_coords[area]['long'], area_coords[area]['lat'], f"{area}\n{column}: {value}", va='bottom', ha='left', fontsize=16,
                         color='blue', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    st.pyplot(map_plot(df_final, texts, font_size, show_lines))
elif option == 'OP':
    df_final = df_final[df_final['LIQUID RATE(BLPD)'] > 0.1]
    column_rename_dict = {"LIQUID RATE(BLPD)": "L blpd", "OIL(BOPD)": "O bopd"}
    df_final.rename(columns=column_rename_dict, inplace=True)
    df_final["L blpd"] = df_final["L blpd"].astype(int)
    df_final["O bopd"] = df_final["O bopd"].astype(int)
    texts = ["L blpd", "O bopd"]
    font_size = 8
elif option == 'GP':
    df_final = df_final[df_final['Free gas'] > 0.1]
    df_final['Free gas'] = df_final['Free gas'].astype(int)
    texts = ['Free gas']
    font_size = 16
elif option == 'WI':
    df_final = df_final[df_final['Injection rate bwpd'] > 0.1]
    column_rename_dict = {'Injection rate bwpd': "WI bwpd"}
    df_final.rename(columns=column_rename_dict, inplace=True)
    df_final["WI bwpd"] = df_final["WI bwpd"].astype(int)
    texts = ["WI bwpd"]
    font_size = 14
elif option == 'GI':
    df_final = df_final[df_final['GAS LIFT RATE(M3/DAY)'] > 0.1]
    column_rename_dict = {'GAS LIFT RATE(M3/DAY)': "GI m3/d"}
    df_final.rename(columns=column_rename_dict, inplace=True)
    df_final["GI m3/d"] = df_final["GI m3/d"].astype(int)
    texts = ["GI m3/d"]
    font_size = 11

st.pyplot(map_plot(df_final, texts, font_size, show_lines))
