#import cartopy
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final.csv"
# Load dataframe here
df_final = pd.read_csv(data_url)  # replace 'your_data.csv' with your dataframe file path


def map_plot(df, texts, color):
    fig, ax = plt.subplots(figsize=(15, 15))

    ax.scatter(df['Longitude'], df['Latitude'], color='blue')

    for i in range(len(df)):
        row = df.iloc[i]
        ax.text(row['Longitude'], row['Latitude'], 
                f"{row['Platform']}\n" + "\n".join([f"{text}: {row[text]}" for text in texts]),
                va='bottom', ha='left', fontsize=16, color=color)

    plt.title('Platform Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    return fig

st.title('NH Asset Platforms')

option = st.sidebar.selectbox('Select Option', ('None', 'OP', 'GP', 'WI'), index=0)

if option == 'None':
    texts = []
    color = 'black'
elif option == 'OP':
    texts = ['LIQUID RATE(BLPD)', 'OIL(BOPD)', 'WATER(BWPD)', 'GAS LIFT RATE(M3/DAY)']
    color = 'black'
elif option == 'GP':
    df_final = df_final[df_final['Free gas'] > 0.1]
    texts = ['Free gas']
    color = 'green'
elif option == 'WI':
    df_final = df_final[df_final['INJECTION RATE(M3/DAY)'] > 0.1]
    texts = ['INJECTION RATE(M3/DAY)']
    color = 'blue'

fig = map_plot(df_final, texts, color)
st.pyplot(fig)

