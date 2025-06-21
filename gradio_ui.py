import gradio as gr
from battery_swap_optimizer import generate_riders, generate_stations, assign_swap_station
import pandas as pd

def run_optimizer(num_riders, num_stations):
    riders_df = generate_riders(num_riders)
    stations_df = generate_stations(num_stations)
    plan_df = assign_swap_station(riders_df, stations_df)

    # Save results
    riders_csv = riders_df.to_csv(index=False)
    stations_csv = stations_df.to_csv(index=False)
    plan_csv = plan_df.to_csv(index=False)

    return riders_df, stations_df, plan_df, plan_csv

with gr.Blocks(title="Battery Swap Routing Optimizer") as demo:
    gr.Markdown("# 🔋 Battery-Swap Routing Optimizer\nMock rider + station data, optimized swap plan")

    with gr.Row():
        num_riders = gr.Slider(minimum=10, maximum=200, value=100, label="Number of Riders")
        num_stations = gr.Slider(minimum=3, maximum=10, value=6, label="Number of Swap Stations")

    run_btn = gr.Button("Run Optimizer")

    with gr.Tab("🧍 Riders Data"):
        rider_output = gr.Dataframe(interactive=False)
    with gr.Tab("🏪 Stations Data"):
        station_output = gr.Dataframe(interactive=False)
    with gr.Tab("✅ Swap Plan Output"):
        plan_output = gr.Dataframe(interactive=False)
        csv_output = gr.File(label="Download Plan CSV")

    def run_all(riders, stations):
        riders_df, stations_df, plan_df, plan_csv = run_optimizer(riders, stations)
        with open("plan_output.csv", "w") as f:
            f.write(plan_csv)
        return riders_df, stations_df, plan_df, "plan_output.csv"

    run_btn.click(run_all, inputs=[num_riders, num_stations], outputs=[rider_output, station_output, plan_output, csv_output])

demo.launch()
