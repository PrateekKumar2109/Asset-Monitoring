#import cartopy
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final.csv"
# Load dataframe here
df_final = pd.read_csv(data_url)  # replace 'your_data.csv' with your dataframe file path


def map_plot(df, texts):
    fig, ax = plt.subplots(figsize=(15, 15))

    ax.scatter(df['Longitude'], df['Latitude'], color='blue')

    for i in range(len(df)):
        row = df.iloc[i]
        ax.text(row['Longitude'], row['Latitude'], 
                "\n".join([f"{text}: {row[text]}" for text in texts]),
                va='bottom', ha='left', fontsize=8,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.title('Platform Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    return fig

st.title('NH Asset Platforms')

option = st.sidebar.selectbox('Select Option', ('OP', 'GP', 'WI'), index=0)

if option == 'OP':
    texts = ['LIQUID RATE(BLPD)', 'OIL(BOPD)', 'WATER(BWPD)', 'GAS LIFT RATE(M3/DAY)']
elif option == 'GP':
    texts = ['Free gas']
elif option == 'WI':
    texts = ['INJECTION RATE(M3/DAY)']

fig = map_plot(df_final, texts)
st.pyplot(fig)

