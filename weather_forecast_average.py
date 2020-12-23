import queue
import threading
import requests
import json
import time

def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(f"Elapsed Time: {time.time() - start}")

    return wrapper

def get_avg_max_temp(q):
    url = q.get()
    req = requests.get(url)
    weather_data = json.loads(req.text)
    city = weather_data["title"]
    max_temps = [
        weather["max_temp"] for weather in weather_data["consolidated_weather"]
    ]
    avg_max_temp = round(sum(max_temps) / len(max_temps), 2)
    print(f"{city} Average Max Temp: {avg_max_temp}")
    q.task_done()


@elapsed_time
def main():
    urls = [
        "https://www.metaweather.com/api/location/2487610/",
        "https://www.metaweather.com/api/location/2442047/",
        "https://www.metaweather.com/api/location/2366355/",
    ]
    q = queue.Queue()
    work_queue = queue.Queue(3)
    threads = []
    for i in range(len(urls)):
        t = threading.Thread(target=get_avg_max_temp, args=(q,))
        t.daemon = True
        t.start()

    for url in urls:
        q.put(url)

    q.join()


if __name__ == "__main__":
    main()
