import matplotlib.pyplot as plt
import numpy as np

def read_time_log(file_path):
    time_log = {}
    with open(file_path, 'r') as file:
        for line in file:
            date, time_info = line.strip().split(": ")
            seconds_open = int(time_info.split()[0])
            time_log[date] = seconds_open
    return  time_log

def plot_time_log(time_log):
    dates = list(time_log.keys())
    times = [seconds / 3600 for seconds in time_log.values()]

    # Balkendiagram wird erstellt
    plt.figure(figsize=(10,6))
    y_pos = np.arange(len(dates))
    plt.bar(y_pos, times, align='center', alpha=0.7)
    plt.xticks(y_pos, dates, rotation=45)
    plt.xlabel('datum')
    plt.ylabel('Geöffnete Stunden')
    plt.title('Dota 2 Laufzeit')

    plt.tight_layout()
    plt.show()

log_file_path = 'program_usage_log.txt'
time_log = read_time_log(log_file_path)
plot_time_log(time_log)