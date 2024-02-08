import os
from pystray import MenuItem as item
import PySimpleGUI as sg
import pystray
from PIL import Image, ImageDraw
import threading
import psutil
import time
from datetime import  datetime



def is_dota_running(program_name):
    for proc in psutil.process_iter(attrs=['name']):
        try:
            if program_name.lower() in proc.info['name'].lower():
                return True
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def read_time_log(file_path):
    if not os.path.exists(file_path):
        return{}
    with open (file_path, 'r') as file:
        lines = file.readlines()
    time_log = {}
    for line in lines:
        date, seconds = line.strip().split(": ")
        time_log[date] = int(seconds)
    return time_log

def write_time_log(file_path, time_log):
    with open(file_path, 'w') as file:
        for date, seconds in time_log.items():
            file.write(f"Tag {date}: {seconds} Sekunden geöffnet\n")


program_name = 'dota2.exe'
log_file_path = 'program_usage_log.txt'
time_log = read_time_log(log_file_path)


program_start_time = None
while True:
    running = is_dota_running(program_name)
    if running and program_start_time is None:
        program_start_time = time.time()
    elif not running and program_start_time is not None:
        program_end_time = time.time()
        elapsed_time = int(program_end_time - program_start_time)
        if elapsed_time > 300:
            today = datetime.now().strftime("%Y-%m-%d")
            if today in time_log:
                time_log[today] += elapsed_time
            else:
                time_log[today] = elapsed_time
            write_time_log(log_file_path, time_log)
            print(f"Zeit für {today} gespeichert: {elapsed_time} Sekunden.")
            program_start_time = None
    time.sleep(60)