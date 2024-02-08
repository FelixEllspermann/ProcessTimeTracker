import psutil
import time

def is_dota_running(program_name):
    for proc in psutil.process_iter(attrs=['name']):
        try:
            if program_name.lower() in proc.info['name'].lower():
                return True
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def read_total_time(file_path):
    try:
        with open(file_path, 'r') as file:
            total_time = int(file.read())
    except FileNotFoundError:
        total_time = 0
    return total_time

def write_total_time(file_path, total_time):
    with open(file_path, 'w') as file:
        file.write(str(total_time))

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600)  // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours} Stunden, {minutes} Minuten, {seconds} Sekunden"
    elif minutes > 0:
        return f"{minutes} Minuten, {seconds} Sekunden"
    else:
        return f"{seconds} Sekunden"


program_name = 'dota2.exe'
file_path = 'program_time.txt'


program_start_time = None
while True:
    running = is_dota_running(program_name)
    if running and program_start_time is None:
        program_start_time = time.time()
    elif not running and program_start_time is not None:
        program_end_time = time.time()

        # berechne Vergangene Zeit seit dem Start des Programmes
        elapsed_time = int(program_end_time - program_start_time)

        #
        total_time = read_total_time(file_path) + elapsed_time
        write_total_time(file_path, total_time)
        formated_time = format_time(elapsed_time)
        total_formated_time = formated_time(total_time)
        print(f"{program_name} lief für {formated_time} Sekunden. Gesamtzeit jetzt: {total_formated_time} Sekunden")
        program_start_time = None
    time.sleep(5)