import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final2.csv"
df_final = pd.read_csv(data_url)  
df_final.loc[df_final['Platform type'].isin(['Process Complex', 'Flare']), 'Free gas'] = 0.0

st.set_page_config(layout="wide") 

def map_plot(df, texts, color, font_size):
    fig, ax = plt.subplots(figsize=(20, 16),dpi=600)  
    ax.set_facecolor('#e6f3ff') 
    ax.scatter(df['Longitude'], df['Latitude'], color='blue', s=60)  

    for i in range(len(df)):
        row = df.iloc[i]
        if texts:
            text = f"{row['Platform']}\n" + "\n".join([f"{text}: {row[text]}" for text in texts])
            if option == 'None' and row['Rig'] == 'yes':
                text_color = 'orange'
            else:
                text_color = color
            ax.text(row['Longitude'], row['Latitude'], text, va='bottom', ha='left', fontsize=font_size, color=text_color,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
        else:
            ax.text(row['Longitude'], row['Latitude'], f"{row['Platform']}", va='bottom', ha='left', fontsize=16,
                    color=color)

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
    color = 'black'
    font_size = 16
elif option == 'OP':
    df_final = df_final[df_final['LIQUID RATE(BLPD)'] > 0.1]
    texts = ['LIQUID RATE(BLPD)', 'OIL(BOPD)']
    color = 'black'
    font_size = 8
elif option == 'GP':
    df_final = df_final[df_final['Free gas'] > 0.1]
    texts = ['Free gas']
    color = 'green'
    font_size = 16
elif option == 'WI':
    df_final = df_final[df_final['INJECTION RATE(M3/DAY)'] > 0.1]
    texts = ['INJECTION RATE(M3/DAY)']
    color = 'blue'
    font_size = 14
elif option == 'GI':
    df_final = df_final[df_final['GAS LIFT RATE(M3/DAY)'] > 0.1]
    texts = ['GAS LIFT RATE(M3/DAY)']
    color = 'red'
    font_size = 11

# Create the map plot and add it to the Streamlit app
st.pyplot(map_plot(df_final, texts, color, font_size))

