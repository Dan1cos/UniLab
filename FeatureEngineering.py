import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the working directory to the script directory
os.chdir(script_dir)

DATA_FILE = "alarms.csv"

# Read in the CSV file and convert the 'start' column to datetime format
df = pd.read_csv(DATA_FILE, delimiter=';', parse_dates=['start'])
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

#print(df.columns)

def regions_at_time(df, day, start_time, end_time):
    """
    Returns the number of regions where events happened at a specific time on a given day.
    df: pandas DataFrame containing the timetable data
    day: string in the format 'YYYY-MM-DD' representing the day to filter by
    start_time: string in the format 'HH:MM' representing the time alarm started to filter by
    end_time: string in the format 'HH:MM' representing the time alaram ended to filter by
    """
    # Filter the DataFrame by the specified day and time range
    mask = (df["start"] >= pd.to_datetime(day + " " + start_time + ":00")) & (df["start"] <= pd.to_datetime(day + " " + end_time + ":59"))
    #return df[mask]["region_id"].unique()
    return len(df[mask]["region_id"].unique())




def events_in_region(df, region_id, day):
    """
    Returns the number of events that occurred in a specific region during a given day (24 hours).
    df: pandas DataFrame containing the timetable data
    region_id: integer representing the region ID to filter by
    day: string in the format 'YYYY-MM-DD' representing the day to filter by
    """
    # Filter the DataFrame by the specified region ID and day
    mask = (df['region_id'] == region_id) & (df["start"].dt.date == pd.to_datetime(day).date())
    df_filtered = df[mask]

    # Count the number of events in the filtered DataFrame
    num_events = len(df_filtered)
    return num_events



#test
"""
num_regions = regions_at_time(df, '2022-04-07', '11:00', '11:59')
print(num_regions)

num_events = events_in_region(df, 3, '2022-03-07')
print(num_events)
"""
