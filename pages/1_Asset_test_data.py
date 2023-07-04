#import cartopy
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
data_url="https://raw.githubusercontent.com/PrateekKumar2109/Asset-Monitoring/main/df_final.csv"
# Load dataframe here
df_final = pd.read_csv(data_url)  # replace 'your_data.csv' with your dataframe file path

st.set_page_config(layout="wide") # Make the layout wide

def map_plot(df, texts, color, font_size):
    fig, ax = plt.subplots(figsize=(20, 16))  # Increase the size of the plot
    ax.set_facecolor('lightgrey') # set light background in the plot
    ax.scatter(df['Longitude'], df['Latitude'], color='blue', s=60)  # Increase the size of the points with s


    for i in range(len(df)):
        row = df.iloc[i]
        if texts:
            text = f"{row['Platform']}\n" + "\n".join([f"{text}: {row[text]}" for text in texts])
            ax.text(row['Longitude'], row['Latitude'], text, va='bottom', ha='left', fontsize=font_size, color=color,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
        else:
            ax.text(row['Longitude'], row['Latitude'], f"{row['Platform']}", va='bottom', ha='left', fontsize=16,
                    color=color)
            
    plt.title('Platform Data', fontsize=24)  # Increase the size of the title
    plt.gca().axes.get_xaxis().set_visible(False)  # Hide x axis
    plt.gca().axes.get_yaxis().set_visible(False)  # Hide y axis

    return fig

st.title('NH Asset Platforms', )

option = st.sidebar.selectbox('Select Option', ('None', 'OP', 'GP', 'WI'), index=0)

if option == 'None':
    texts = []
    color = 'black'
    font_size = 16
elif option == 'OP':
    texts = ['LIQUID RATE(BLPD)', 'OIL(BOPD)', 'WATER(BWPD)', 'GAS LIFT RATE(M3/DAY)']
    color = 'black'
    font_size = 8
elif option == 'GP':
    df_final = df_final[df_final['Free gas'] > 0.1]
    texts = ['Free gas']
    color = 'green'
    font_size = 14
elif option == 'WI':
    df_final = df_final[df_final['INJECTION RATE(M3/DAY)'] > 0.1]
    texts = ['INJECTION RATE(M3/DAY)']
    color = 'blue'
    font_size = 10

fig = map_plot(df_final, texts, color, font_size)
st.pyplot(fig)



