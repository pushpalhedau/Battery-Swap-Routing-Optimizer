import pandas as pd
import numpy as np
from geopy.distance import geodesic
from datetime import datetime, timedelta
import random

# --- CONFIGURATION ---
NUM_RIDERS = 100
NUM_STATIONS = 6
PUNE_CENTER = (18.5204, 73.8567)  # Central Pune coordinates
SOC_USAGE_PER_KM = 4  # 4% SOC per km
MAX_QUEUE_LEN = 5
SWAP_DURATION_MIN = 4

# --- MOCK DATA GENERATION ---
def generate_riders(num=NUM_RIDERS):
    riders = []
    for i in range(num):
        rider_id = f"R{i:03}"
        lat = PUNE_CENTER[0] + np.random.uniform(-0.02, 0.02)
        lng = PUNE_CENTER[1] + np.random.uniform(-0.02, 0.02)
        soc_pct = np.random.randint(5, 100)
        status = random.choice(["idle", "on_gig"])
        km_to_finish = round(np.random.uniform(0.5, 5.0), 2) if status == "on_gig" else 0.0
        est_finish_ts = datetime.now() + timedelta(minutes=random.randint(5, 30))
        riders.append({
            "rider_id": rider_id,
            "lat": lat,
            "lng": lng,
            "soc_pct": soc_pct,
            "status": status,
            "km_to_finish": km_to_finish,
            "est_finish_ts": est_finish_ts,
        })
    return pd.DataFrame(riders)

def generate_stations(num=NUM_STATIONS):
    stations = []
    for i in range(num):
        station_id = f"S_{chr(65+i)}"
        lat = PUNE_CENTER[0] + np.random.uniform(-0.03, 0.03)
        lng = PUNE_CENTER[1] + np.random.uniform(-0.03, 0.03)
        queue_len = random.randint(0, MAX_QUEUE_LEN - 1)
        stations.append({
            "station_id": station_id,
            "lat": lat,
            "lng": lng,
            "queue_len": queue_len,
        })
    return pd.DataFrame(stations)

# --- OPTIMIZATION LOGIC ---
def assign_swap_station(riders_df, stations_df):
    output = []
    for _, rider in riders_df.iterrows():
        if rider['soc_pct'] < 10 or \
           (rider['status'] == 'on_gig' and rider['soc_pct'] - rider['km_to_finish'] * SOC_USAGE_PER_KM < 10):

            # Calculate distance to each station
            stations_df['distance_km'] = stations_df.apply(
                lambda s: geodesic((rider['lat'], rider['lng']), (s['lat'], s['lng'])).km, axis=1
            )
            # Filter by queue capacity
            eligible_stations = stations_df[stations_df['queue_len'] < MAX_QUEUE_LEN]
            if eligible_stations.empty:
                continue

            # Choose nearest station
            nearest_station = eligible_stations.sort_values(by='distance_km').iloc[0]

            # Estimate timestamps
            travel_time_min = nearest_station['distance_km'] / 0.3 * 60  # 18 km/h avg
            depart_ts = datetime.now()
            arrive_ts = depart_ts + timedelta(minutes=travel_time_min)
            swap_start_ts = arrive_ts
            swap_end_ts = swap_start_ts + timedelta(minutes=SWAP_DURATION_MIN)

            eta_back_lat = rider['lat']
            eta_back_lng = rider['lng']

            output.append({
                "rider_id": rider['rider_id'],
                "station_id": nearest_station['station_id'],
                "depart_ts": depart_ts,
                "arrive_ts": arrive_ts,
                "swap_start_ts": swap_start_ts,
                "swap_end_ts": swap_end_ts,
                "eta_back_lat": eta_back_lat,
                "eta_back_lng": eta_back_lng
            })

            # Update queue length
            stations_df.loc[stations_df['station_id'] == nearest_station['station_id'], 'queue_len'] += 1

    return pd.DataFrame(output)

if __name__ == "__main__":
    riders = generate_riders()
    stations = generate_stations()
    plan = assign_swap_station(riders, stations)

    # Save outputs
    riders.to_csv("mock_riders.csv", index=False)
    stations.to_csv("mock_stations.csv", index=False)
    plan.to_csv("plan_output.csv", index=False)

    print("Optimization complete. Output saved to plan_output.csv")
