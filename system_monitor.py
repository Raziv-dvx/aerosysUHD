import psutil
import datetime
import time

class SystemMonitor:
    def __init__(self):
        self.cpu_usage = 0
        self.ram_usage = 0
        self.gpu_usage = 0
        self.disk_usage = 0
        self.network_upload = "0 KB/s"
        self.network_download = "0 KB/s"
        self.temperature = 0
        self.battery_level = 0
        self.current_time = "00:00:00"
        self.current_date = "January 1, 2024"
        
        # Network stats
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
    def update_all(self):
        self.update_cpu()
        self.update_ram()
        self.update_gpu()
        self.update_disk()
        self.update_network()
        self.update_temperature()
        self.update_battery()
        self.update_time()
        
    def update_cpu(self):
        self.cpu_usage = int(psutil.cpu_percent(interval=0.1))
        
    def update_ram(self):
        self.ram_usage = int(psutil.virtual_memory().percent)
        
    def update_gpu(self):
        # Simple GPU monitoring - in a real app you might use GPUtil or nvidia-smi
        try:
            # This is a placeholder - actual implementation would vary
            self.gpu_usage = min(100, self.cpu_usage + 10)  # Fake data for demo
        except:
            self.gpu_usage = 0
            
    def update_disk(self):
        self.disk_usage = int(psutil.disk_usage('/').percent)
        
    def update_network(self):
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_net_time
        
        if time_diff > 0:
            upload_speed = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff
            download_speed = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
            
            self.network_upload = self.format_speed(upload_speed)
            self.network_download = self.format_speed(download_speed)
            
        self.last_net_io = current_net_io
        self.last_net_time = current_time
        
    def format_speed(self, speed):
        if speed < 1024:
            return f"{int(speed)} B/s"
        elif speed < 1024 * 1024:
            return f"{int(speed / 1024)} KB/s"
        else:
            return f"{int(speed / (1024 * 1024))} MB/s"
            
    def update_temperature(self):
        try:
            # This varies by system - might not work on all Windows machines
            temps = psutil.sensors_temperatures()
            if temps and 'coretemp' in temps:
                self.temperature = int(temps['coretemp'][0].current)
            else:
                self.temperature = 40  # Default fallback
        except:
            self.temperature = 40
            
    def update_battery(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.battery_level = int(battery.percent)
            else:
                self.battery_level = 100
        except:
            self.battery_level = 100
            
    def update_time(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        self.current_date = now.strftime("%B %d, %Y")