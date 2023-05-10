import os
from dotenv import load_dotenv  # if missing this module, simply run `pip install python-dotenv`
import requests

load_dotenv()
API_KEY = os.getenv('NASDAQ_API_KEY')

qry_params = "start_date=2017-01-01&end_date=2017-12-31&api_key="
url = "https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X/data.json?" + qry_params + API_KEY


def find_median(arr):
    sorted_arr = sorted(arr)
    print(sorted_arr)
    if len(sorted_arr) % 2 != 0:
        # odd number of items, so just pick out the median
        median = sorted_arr[len(sorted_arr) // 2]
    else:
        mid_low_ind = len(sorted_arr) // 2 - 1
        mid_low = sorted_arr[mid_low_ind]
        mid_high = sorted_arr[mid_low_ind + 1]
        print(mid_high, mid_low)
        median = (mid_high + mid_low) / 2
    return median


# Make the API request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    # Process the response data
    print(data)
    open_prices = []
    daily_diff = []
    closing = []
    volume = []
    for arr in data["dataset_data"]["data"]:
        if arr[1]:
            open_prices.append(arr[1])
        if arr[2] and arr[3]:
            daily_diff.append(abs(arr[2] - arr[3]))
        if arr[4]:
            closing.append(arr[4])
        if arr[6]:
            volume.append(arr[6])
    if volume:
        avg_volume = sum(volume) / len(volume)
        median = find_median(volume)

    print("Highest opening price in this period: {}".format(max(open_prices)))
    print("Lowest opening price in this period: {}".format(min(open_prices)))
    print("Largest change in any one day: {}".format(max(daily_diff)))
    print("Largest change between any two days based on closing price: {}".format(max(closing) - min(closing)))
    print("Average daily trading volume: {}".format(avg_volume))
    print("Median trading volume: {}".format(median))
else:
    print("Error:", response.status_code)
