import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final3.csv"
df_fin = pd.read_csv(data_url)  
#df_final.loc[df_final['Platform type'].isin(['Process Complex', 'Flare']), 'Free gas'] = 0.0
df_final = df_fin[df_fin["Platform type"] == "Well head"]
st.set_page_config(layout="wide") 

def map_plot(df, texts, font_size):
    fig, ax = plt.subplots(figsize=(20, 16),dpi=600)  
    ax.set_facecolor('#e6f3ff') 

    # Create a scatter plot with different colors for each 'Field' value
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

    # Define lines details
    lines = [
        {"start_lat": 18.72, "start_lon": 72.315, "length": 0.04, "angle": 30},
        {"start_lat": 18.77, "start_lon": 72.29, "length": 0.05, "angle": -13},
        {"start_lat": 18.50, "start_lon": 72.24, "length": 0.04, "angle": 12},
        {"start_lat": 18.609, "start_lon": 72.259, "length": 0.08, "angle": 145}
    ]

    # Add dashed lines
    for line in lines:
        angle_rad = np.deg2rad(line["angle"])
        end_lat = line["start_lat"] + line["length"] * np.sin(angle_rad)
        end_lon = line["start_lon"] + line["length"] * np.cos(angle_rad)
        plt.plot([line["start_lon"], end_lon], [line["start_lat"], end_lat], linestyle='dashed', color='black')

    plt.title(' Offshore Platforms', fontsize=24)  
    plt.gca().axes.get_xaxis().set_visible(False)  
    plt.gca().axes.get_yaxis().set_visible(False) 

    return fig

st.title('NH Asset Platforms')

option = st.sidebar.selectbox('Select Option', ('None', 'OP', 'GP', 'WI', 'GI'), index=0)

if option == 'None':
    texts = []
    font_size = 16
elif option == 'OP':
    df_final = df_final[df_final['LIQUID RATE(BLPD)'] > 0.1]
    # Rename the columns
    column_rename_dict = {"LIQUID RATE(BLPD)": "L blpd", "OIL(BOPD)": "O bopd"}
    df_final.rename(columns=column_rename_dict, inplace=True)
    # Convert the float values in the "L blpd" and "O bopd" columns to integers
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
    df_final["GI m3/d"] = df_final["GI m3/d"].astype(int)
    df_final.rename(columns=column_rename_dict, inplace=True)
    texts = ["GI m3/d"]
    font_size = 11

# Create the map plot and add it to the Streamlit app
st.pyplot(map_plot(df_final, texts, font_size))
