import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final2.csv"
# Load dataframe here
df_final = pd.read_csv(data_url)  
# Setting 'Free gas' value to 0.0 where 'Platform type' is either 'Process Complex' or 'Flare'
df_final.loc[df_final['Platform type'].isin(['Process Complex', 'Flare']), 'Free gas'] = 0.0

# Display the rows where 'Platform type' is 'Process Complex' or 'Flare'
display_rows = df_final[df_final['Platform type'].isin(['Process Complex', 'Flare'])]

print(display_rows)

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
    # Add a dashed line
    start_lat = 18.710
    start_lon = 72.315
    angle = np.deg2rad(30)  # Convert the angle to radians
    # Length of the line
    length = 0.1  # Change this value to adjust the length of the line
    end_lat = start_lat + length * np.sin(angle)
    end_lon = start_lon + length * np.cos(angle)
    plt.plot([start_lon, end_lon], [start_lat, end_lat], linestyle='dashed', color='black')
            
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
