import time
import signal
import sys
import logging
import yaml
import os
from .monitor import SystemMonitor
from .analyzer import ProcessAnalyzer
from .logger import setup_logging

class CyberAgent:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.logger = setup_logging(self.config)
        self.monitor = SystemMonitor(self.logger)
        self.analyzer = ProcessAnalyzer(self.config, self.logger)
        self.running = True

    def _load_config(self, path):
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def start(self):
        self.logger.info("Cyber Agent starting with root privileges...")
        
        # Ensure we are running as root
        if os.geteuid() != 0:
            self.logger.warning("Agent is NOT running as root! Some capabilities will be limited.")
        
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        while self.running:
            try:
                self.run_cycle()
                time.sleep(self.config['agent']['scan_interval'])
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(5)

    def run_cycle(self):
        """
        Main monitoring cycle.
        """
        # 1. Get all running processes
        processes = self.monitor.get_processes()
        
        # 2. Analyze processes
        suspicious_list = self.analyzer.analyze(processes)
        
        # 3. Take action (Simulated for now unless configured)
        if suspicious_list:
            for proc_info in suspicious_list:
                self.logger.warning(f"Suspicious Activity Detected: {proc_info['name']} (PID: {proc_info['pid']}) - Reason: {proc_info['reason']}")
                # Future: Implement auto-kill logic here if enabled in config
                
        # 4. Check system health
        health = self.monitor.get_system_health()
        if health['cpu'] > self.config['security']['max_cpu_percent']:
             self.logger.warning(f"High System CPU Usage: {health['cpu']}%")

    def stop(self, signum=None, frame=None):
        self.logger.info("Stopping Cyber Agent...")
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    # Assuming config is relative to the script for simplicity in dev, 
    # but in prod it should be /etc/cyber-agent/settings.yaml
    config_path = os.path.join(os.path.dirname(__file__), '../config/settings.yaml')
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    agent = CyberAgent(config_path)
    agent.start()
