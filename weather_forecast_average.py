import threading
import requests
import json


def get_avg_max_temp(url):
    req = requests.get(url)
    weather_data = json.loads(req.text)
    city = weather_data["title"]
    max_temps = [
        weather["max_temp"] for weather in weather_data["consolidated_weather"]
    ]
    avg_max_temp = round(sum(max_temps) / len(max_temps), 2)
    print(f"{city} Average Max Temp: {avg_max_temp}")


def main():
    urls = [
        "https://www.metaweather.com/api/location/2487610/",
        "https://www.metaweather.com/api/location/2442047/",
        "https://www.metaweather.com/api/location/2366355/",
    ]
    for url in urls:
        t = threading.Thread(target=get_avg_max_temp, args=(url,))
        t.start()


if __name__ == "__main__":
    main()
