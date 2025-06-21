
# 🔋 Battery-Swap Routing Optimizer

Smart optimizer to guide electric bike riders on when and where to swap their battery based on battery state, location, delivery status, and station load.

Built as part of an AI/ML internship challenge focused on real-world mobility and logistics optimization.

---

## 📌 Features

- 🔓 Automatically assigns at-risk riders to the nearest available station
- 🔐 Queuing and scheduling based on swap time slots
- ✏️ Exportable schedule output with timestamps and location data
- 🗃️ Scalable to larger cities by increasing station count

---

## 📂 Project Structure
```Project Structure 
├── battery_swap_optimizer.py # Core logic and mock data generation 
├── plan_output.csv # Final output for eligible riders 
├── solution.md # Assumptions, approach, algorithm 
├── gradio_ui.py # Interactive UI built with Gradio
├── requirements.txt # Python dependencies 
└── README.md # Project overview
```

---

## 🚀 How to Run

### Option 1: From Command Line

```bash
pip install -r requirements.txt
python battery_swap_optimizer.py
```

Output saved as plan_output.csv (as asked in the problem statement)


### Option 2: Interactive Gradio UI
```bash
pip install -r requirements.txt
pip install gradio pandas geopy
python gradio_ui.py
```

A web UI will open in your browser where you can:

**Note: If it doesn't work on system, try running both python files on google collab(comment 2nd line in gradio_ui.py).**
- Select rider/station count

- Run optimizer

- View rider/station/swap tables

- Download final plan as CSV

## CSV

📥 Inputs

Mock data is generated automatically:

Riders:

-  `rider_id`,  `lat `,  `lng `,  `soc_pct `,  `status `,  `km_to_finish `,  `est_finish_ts `

Stations:

`station_id`, `lat`, `lng`, `queue_len`

## ✅ Goals

- ⚡ Avoid battery dropping below 10% (SOC Rule)

- 📍 Minimize travel overhead to swap (Efficiency Rule)

- 🚦 Max 5 riders in queue per station (Queue Rule)

## 🧠 Optimization Logic

- Filter riders who are below safe SOC threshold

- Rank nearby stations by distance and queue availability

- Schedule each rider to a slot, respecting 4-min swap duration

## 🔮 Future Enhancements

- Integrate Google Maps API or OpenRouteService for actual routes

- Incorporate delivery urgency scores

- Predict queue times using ML

- Add map visualization and heatmaps

## 👤 Author
Pushpal Hedau
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pushpal-hedau-04479124a/)
