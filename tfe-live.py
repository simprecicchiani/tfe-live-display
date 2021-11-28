import requests 
from datetime import timedelta, date, datetime 
import pytz

def get_buses_coming_soon(stop_id): 
    apiurl = f"https://tfe-opendata.com/api/v1/live_bus_times/{stop_id}" 
    response = requests.request("GET", apiurl) 
    all_busses = response.json() 
    return all_busses

def time_till(dep_time):
    delta = datetime.fromisoformat(dep_time) - timedelta(hours=1) - datetime.now(pytz.timezone('Europe/London'))
    return int(delta.seconds/60)

def display_line(name='', destination='', time=''):
    if type(time) != str:
        time = str('DUE' if time < 1 else (99 if time > 99 else time))
    print(f"{name:<3.3} {destination:<16.16} {time:>3.3}")

def next_buses(stop_id):
    data = get_buses_coming_soon(stop_id)
    display_lines = 2
    print(f"{'bus':<3} {'Destination':^15} {'mins':>4}")
    for route in data:
        name = route['routeName']
        destinations = route['departures']
        for line in range(display_lines):
            try:
                destination = destinations[line]['destination']
                departure_time = destinations[line]['departureTime']
                due_in = time_till(departure_time)
                display_line(name, destination, due_in)
            except IndexError:
                display_line()
                pass
        print("-"*24)

next_buses(36232574)

