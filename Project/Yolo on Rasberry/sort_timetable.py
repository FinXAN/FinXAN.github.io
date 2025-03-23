import os
import pandas as pd
from datetime import datetime, timedelta

def generate_timetable(directory, output_file):
    files = [f for f in os.listdir(directory) if f.endswith(".png")]
    
    # Extract timestamps from filenames
    data = []
    for file in files:
        parts = file.split("_")
        if len(parts) == 3 and parts[1].isdigit() and parts[2].endswith(".png"):
            try:
                timestamp = datetime.strptime(parts[1] + "_" + parts[2].split(".")[0], "%Y%m%d_%H%M%S")
                data.append((timestamp, file))
            except ValueError as e:
                print(f"Skipping file {file} due to incorrect format: {e}")
    data.sort()

    # Group trains within 2-minute slots
    timetable = {}
    slot_start = None
    grouped_trains = []

    for timestamp, file in data:
        if slot_start is None or (timestamp - slot_start) > timedelta(minutes=2):
            if grouped_trains:
                earliest_timestamp = grouped_trains[0][0]  
                date_str = earliest_timestamp.strftime("%Y-%m-%d")
                hour_str = earliest_timestamp.strftime("%I %p")  # 12-hour format with AM/PM
                time_slot = earliest_timestamp.strftime("%I:%M %p")  # Earliest timestamp defines slot

                if date_str not in timetable:
                    timetable[date_str] = {}
                if hour_str not in timetable[date_str]:
                    timetable[date_str][hour_str] = {}
                if time_slot not in timetable[date_str][hour_str]:
                    timetable[date_str][hour_str][time_slot] = []

                timetable[date_str][hour_str][time_slot].extend([f for _, f in grouped_trains])
            

            slot_start = timestamp
            grouped_trains = [(timestamp, file)]
        else:

            grouped_trains.append((timestamp, file))


    if grouped_trains:
        earliest_timestamp = grouped_trains[0][0]
        date_str = earliest_timestamp.strftime("%Y-%m-%d")
        hour_str = earliest_timestamp.strftime("%I %p")
        time_slot = earliest_timestamp.strftime("%I:%M %p")

        if date_str not in timetable:
            timetable[date_str] = {}
        if hour_str not in timetable[date_str]:
            timetable[date_str][hour_str] = {}
        if time_slot not in timetable[date_str][hour_str]:
            timetable[date_str][hour_str][time_slot] = []

        timetable[date_str][hour_str][time_slot].extend([f for _, f in grouped_trains])

    # Convert to DataFrame and write to Excel
    writer = pd.ExcelWriter(output_file, engine='openpyxl')

    for date, hours in timetable.items():
        df_list = []
        for hour, slots in hours.items():
            for time_slot, files in slots.items():
                df_list.append([hour, time_slot, ", ".join(files)])

        df = pd.DataFrame(df_list, columns=["Hour", "Time Slot", "Files"])
        df.to_excel(writer, sheet_name=date, index=False)

    writer.close()
    print(f"Timetable saved to {output_file}")

## Example:
directory = "./data_set" 
output_file = "train_timetable.xlsx"


generate_timetable(directory, output_file)
