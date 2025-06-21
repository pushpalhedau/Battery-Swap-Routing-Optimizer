
# 🧠 Battery-Swap Routing Optimizer – solution.md

## 🔍 Problem Overview

Electric bike riders must keep their battery charge (SOC) above 10% and swap it at designated stations with minimal travel overhead. Each swap station can handle a maximum of 5 riders at a time, and each swap takes 4 minutes. The optimizer must create a plan valid for the next 60 minutes, guiding riders where and when to swap batteries.

---

## ✅ Objective Summary

- **SOC Rule:** Ensure battery never drops below 10%.
- **Efficiency Rule:** Minimize extra travel distance.
- **Queue Rule:** Ensure no more than 5 riders are scheduled at the same station at the same time.

---

## 🔧 Assumptions

| Parameter       | Value              |
|-----------------|--------------------|
| Riders/hour     | 100 riders         |
| Stations        | 6 stations (not 3) |
| SOC consumption | 4% per km          |
| Swap duration   | 4 minutes          |
| Avg speed       | ~18 km/h           |

- I have increased station count from 3 to 6 for full Pune coverage, ensuring all riders can reach a station within the SOC safety margin (~22 km).

- Geospatial data is mocked around Pune using randomized coordinates.

-Road distance approximated using haversine (geopy) and simple time = distance / speed logic.

---

## 🧮 Data Mocking

### Generated using Python:

- **Riders:** Random SOC (5–100%), status (idle/on_gig), location, gig distance, and finish time.

- **Stations:** Random queue (0–4), with scattered locations across Pune.

### 🧠 Optimization Logic

1. Filter at-risk riders:

- Riders with current SOC < 10%

- Or those who, after completing gig, will drop below 10% SOC

2. Evaluate all stations:

- Compute geodesic distance from rider to each station

- Filter out stations with full queue (>= 5)

3. Select best station:

- Pick nearest station with a queue slot

- Calculate ETA, swap start/end time, and return location

4. Update state:

- Increase queue count at selected station

- Repeat for next eligible rider


## 🖥️ UI & Usability

Built an intuitive Gradio UI that lets users:

- Select number of riders and stations

- View all rider/station/schedule data in tabs

- Download the plan output as a CSV

## 📈 Scalability Ideas

- Integrate real-time SOC, GPS & traffic APIs

- Use a true routing engine (e.g. OpenRouteService or OSRM)

- Prioritize delivery urgency via scoring system

- Implement queue prediction using ML or simulation

- Parallelize optimization using multiprocessing or async

## 📦 Deliverables

- **battery_swap_optimizer.py:** Optimization logic

- **gradio_ui.py:** Web UI with user controls and download option

- **plan_output.csv:** Final schedule for all eligible riders

- **solution.md:** This solution explanation

## 👤 Author
Pushpal Hedau
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pushpal-hedau-04479124a/)
