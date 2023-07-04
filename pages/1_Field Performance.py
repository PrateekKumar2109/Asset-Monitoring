import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Load dataframe here
df_final = pd.read_csv('your_data.csv')  # replace 'your_data.csv' with your dataframe file path

def map_plot(df, texts):
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw=dict(projection=ccrs.PlateCarree()))

    ax.set_extent([df['Longitude'].min()-1, df['Longitude'].max()+1, 
                   df['Latitude'].min()-1, df['Latitude'].max()+1])

    ax.coastlines(resolution='50m')
    ax.gridlines(draw_labels=True)

    for i in range(len(df)):
        row = df.iloc[i]
        ax.scatter(row['Longitude'], row['Latitude'], color='blue')
        ax.text(row['Longitude'], row['Latitude'], 
                "\n".join([f"{text}: {row[text]}" for text in texts]),
                va='bottom', ha='left', fontsize=8,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    plt.title('Platform Data')
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
