import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


today = datetime.now()
week_ago = today - timedelta(days=7)

start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")


url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude=48.85&longitude=2.35"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min"
)

response = requests.get(url)
data = response.json()


daily_data = data["daily"]

df = pd.DataFrame({
    "date": daily_data["time"],
    "max_temp": daily_data["temperature_2m_max"],
    "min_temp": daily_data["temperature_2m_min"]
})

df["date"] = pd.to_datetime(df["date"])

print(df)


plt.figure(figsize=(10, 6))

plt.plot(df["date"], df["max_temp"], marker="o", label="Max Temp")
plt.plot(df["date"], df["min_temp"], marker="o", label="Min Temp")

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Paris Weather - Past 7 Days")
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("weather_chart.png")
plt.show()
 

if not os.path.exists('data'):
    os.makedirs('data')


df.to_csv('data/paris_weather.csv', index=False)
print("Data saved to data/paris_weather.csv")