import psutil
import logging

class SystemMonitor:
    def __init__(self, logger):
        self.logger = logger

    def get_processes(self):
        """
        Retrieves a list of running processes with details.
        """
        process_list = []
        try:
            # Iterate over all running processes
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'exe']):
                try:
                    pinfo = proc.info
                    process_list.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            self.logger.error(f"Error retrieving processes: {e}")
        
        return process_list

    def get_system_health(self):
        """
        Retrieves system-wide health metrics.
        """
        try:
            return {
                'cpu': psutil.cpu_percent(interval=None),
                'memory': psutil.virtual_memory().percent,
                'disk': psutil.disk_usage('/').percent
            }
        except Exception as e:
            self.logger.error(f"Error retrieving system health: {e}")
            return {'cpu': 0, 'memory': 0, 'disk': 0}
