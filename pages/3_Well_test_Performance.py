import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the seaborn style
sns.set_theme()

# Load data
data_url = "https://raw.githubusercontent.com/PrateekKumar2109/Assset-production-monitoring/main/Data/merged_data%20(2).csv"
merged_data = pd.read_csv(data_url)

# Ensure the 'TEST DATE' column is in datetime format
merged_data['TEST DATE'] = pd.to_datetime(merged_data['TEST DATE'])

# Sidebar
st.sidebar.title("Filters")

field_filter = st.sidebar.selectbox("Field", ["Neelam", "Heera", "nan"])
type_filter = st.sidebar.selectbox("Type", ['OP', 'WI', 'GP', 'NA'])
flowing_closed_filter = st.sidebar.selectbox("Flowing/Closed", ['Flowing', 'Closed'])

# Apply filters to the dataframe based on sidebar inputs
if type_filter == 'OP':
    op_filter = st.sidebar.slider('OIL(BOPD)', min_value=0.0, max_value=merged_data['OIL(BOPD)'].max(), value=100.0)
    filtered_data = merged_data[(merged_data['Field'] == field_filter) & (merged_data['Type'] == type_filter) & 
                                 (merged_data['Flowing/Closed'] == flowing_closed_filter) & (merged_data['OIL(BOPD)'] >= op_filter)]
elif type_filter == 'WI':
    wi_filter = st.sidebar.slider('Injection rate bwpd', min_value=0.0, max_value=merged_data['Injection rate bwpd'].max(), value=1000.0)
    filtered_data = merged_data[(merged_data['Field'] == field_filter) & (merged_data['Type'] == type_filter) & 
                                 (merged_data['Flowing/Closed'] == flowing_closed_filter) & (merged_data['Injection rate bwpd'] >= wi_filter)]
elif type_filter == 'GP':
    gp_filter = st.sidebar.slider('Free gas', min_value=0.0, max_value=merged_data['Free gas'].max(), value=20000.0)
    filtered_data = merged_data[(merged_data['Field'] == field_filter) & (merged_data['Type'] == type_filter) & 
                                 (merged_data['Flowing/Closed'] == flowing_closed_filter) & (merged_data['Free gas'] >= gp_filter)]

# Find the latest date for each WELL STRING in the filtered data
latest_dates = filtered_data.groupby('WELL STRING')['TEST DATE'].idxmax()

# Get the corresponding WELL STRING values
latest_well_strings = filtered_data.loc[latest_dates]['WELL STRING'].unique()

# Display the count of "WELL STRING" column values based on the filters
st.title(f"Filtered WELL STRING values")
st.write(latest_well_strings)
st.write(f"Total count: {len(latest_well_strings)}")

# Filter the original dataframe based on these WELL STRING values
filtered_merged_data = merged_data[merged_data['WELL STRING'].isin(latest_well_strings)]

# Interactive plots
st.title(f"Interactive plots based on filters")

for well_string in latest_well_strings:
    st.markdown(f"## {well_string}")
    well_data = filtered_merged_data[filtered_merged_data['WELL STRING'] == well_string]
    
    if type_filter == 'OP':
        fig, axs = plt.subplots(2, figsize=(10, 10))
        sns.lineplot(x='TEST DATE', y='OIL(BOPD)', data=well_data, ax=axs[0])
        axs[0].set_title('OIL(BOPD) over time')
        sns.lineplot(x='TEST DATE', y='LIQUID RATE(BLPD)', data=well_data, ax=axs[1])
        axs[1].set_title('LIQUID RATE(BLPD) over time')
        plt.tight_layout()
        st.pyplot(fig)
    elif type_filter == 'WI':
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='TEST DATE', y='Injection rate bwpd', data=well_data, ax=ax)
        ax.set_title('Injection rate bwpd over time')
        st.pyplot(fig)
    elif type_filter == 'GP':
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='TEST DATE', y='Free gas', data=well_data, ax=ax)
        ax.set_title('Free gas over time')
        st.pyplot(fig)

