import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

# Load the API key from a JSON file
with open("D:/api.json") as f:
    api_key = json.load(f)['api']
    
# API link to the BLS API
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
headers = {'Content-Type': 'application/json'}

# Payload with required series ID (e.g., "CUUR0000SA0" for CPI-U All Urban Consumers)
payload = {
    "seriesid": ["CUSR0000SAF1"],
    "startyear": "2012",
    "endyear": "2024",
    "registrationkey": api_key
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    response_json = response.json()
    response_data = response_json['Results']['series'][0]['data']
    df = pd.DataFrame(response_data)
else:
    print(f"Error: {response.status_code} - {response.text}")


df['month'] = df['period'].str[1:].astype(int)
df['date'] = pd.to_datetime(df[['year','month']].assign(day=1))  # set day=1 for each month
df = df.sort_values('date')  # Ens

df['value'] = pd.to_numeric(df['value'], errors='coerce')

df['month_to_month_inflation'] = df['value'].pct_change() * 100
# Plot the month-to-month inflation
plt.figure(figsize=(10,6))
plt.plot(df['date'], df['month_to_month_inflation'], marker='o', linestyle='-', color='#6699FF', label='Democrats', drawstyle='steps-post')  
plt.plot(df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2020)]['date'], df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2020)]['month_to_month_inflation'], marker='o', linestyle='-', color='#FF6666', label='Republicans', drawstyle='steps-post')  # Darker blue
plt.title('Month-to-Month Inflation')
plt.xlabel('Date')
plt.ylabel('Inflation Rate (%)')
plt.grid(True)
plt.axhline(y=0, color='red', linestyle='--')  # Line at 0% for reference
plt.legend()
plt.show()




# Plot the month-to-month inflation
plt.figure(figsize=(10,6))
plt.plot(df['date'], df['value'], marker='o', linestyle='-', color='#FF6666')  # Darker red
plt.title('Price Level Over Time')
plt.xlabel('Date')
plt.ylabel('Price (CPI Index)')
plt.grid(True)
plt.plot(df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2020)]['date'], df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2020)]['value'], marker='o', linestyle='-', color='#6699FF')  # Darker blue
plt.axhline(y=0, color='red', linestyle='--')  # Line at 0% for reference
plt.ylim(225, 350)

# Add vertical lines
plt.axvline(x=pd.to_datetime('2016-01-01'), color='red', linestyle='--')
plt.axvline(x=pd.to_datetime('2021-01-01'), color='blue', linestyle='--')

plt.show()
