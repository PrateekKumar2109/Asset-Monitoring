import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and favicon
st.set_page_config(page_title="Production Data Dashboard", page_icon=":oil_drum:")

# Load the data
# Note: Replace this with your actual file path
data_url="https://raw.githubusercontent.com/PrateekKumar2109/Assset-production-monitoring/main/Data/my_data.csv"
df = pd.read_csv(data_url)

# Convert the 'DATE' column to datetime format
df['DATE'] = pd.to_datetime(df['DATE'])

# Define the names of the platforms and the corresponding column indices
platforms = {
    'Heera': slice(1, 13),
    'Ratna': slice(13, 18),
    'Neelam': slice(18, 27),
    'B173A': slice(27, 32),
    'B134A': slice(32, 36),
    'NWB173': slice(36, 40),
    'Asset': slice(40, 48)
}

# Define the names of the metrics to be plotted
metrics = ['Liquid , blpd', 'Oil,bopd', 'Total Gas,  MMSCMD']

st.title("Production Data Dashboard")

# Create a sidebar for deselecting the platforms
st.sidebar.markdown("## Select Platforms")
selected_platforms = st.sidebar.multiselect('', list(platforms.keys()), default=list(platforms.keys()))

# Create a sidebar for deselecting the metrics
st.sidebar.markdown("## Select Metrics")
selected_metrics = st.sidebar.multiselect('', metrics, default=metrics)

# Create the plots
for platform in selected_platforms:
    st.header(platform)
    
    for metric in selected_metrics:
        # Select the appropriate columns for the current platform
        cols = df.columns[platforms[platform]]
        
        # Filter out the columns that match the current metric
        metric_cols = [col for col in cols if metric in col]
        
        # Plot the data for the current platform and metric
        for col in metric_cols:
            fig = px.line(df, x='DATE', y=col, title=f'{platform} - {col}')
            fig.update_xaxes(rangeslider_visible=True)
            st.plotly_chart(fig)

