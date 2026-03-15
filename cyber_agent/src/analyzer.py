import logging

class ProcessAnalyzer:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        # Convert list to set for O(1) lookups
        self.whitelist = set(config['security'].get('whitelist', []))
        self.blacklist_patterns = config['security'].get('blacklist_patterns', [])
        self.max_cpu = config['security'].get('max_cpu_percent', 90.0)

    def analyze(self, processes):
        """
        Analyzes the list of processes and returns suspicious ones.
        """
        suspicious_list = []
        
        for proc in processes:
            try:
                # Basic info extraction
                pid = proc.get('pid')
                name = proc.get('name', '')
                cmdline = proc.get('cmdline', [])
                exe = proc.get('exe', '')
                cpu_percent = proc.get('cpu_percent', 0.0)

                # 1. Check Whitelist (Skip analysis if whitelisted)
                if name in self.whitelist:
                    continue

                reason = None

                # 2. Check Blacklist Patterns
                for pattern in self.blacklist_patterns:
                    if pattern in name:
                        reason = f"Process name matches blacklist pattern '{pattern}'"
                        break
                    if cmdline and any(pattern in arg for arg in cmdline):
                        reason = f"Command line argument matches blacklist pattern '{pattern}'"
                        break
                
                if reason:
                    suspicious_list.append({
                        'pid': pid,
                        'name': name,
                        'reason': reason,
                        'details': proc
                    })
                    continue

                # 3. Check High Resource Usage
                if cpu_percent > self.max_cpu:
                    suspicious_list.append({
                        'pid': pid,
                        'name': name,
                        'reason': f"Changes excessive CPU usage: {cpu_percent}% > {self.max_cpu}%",
                        'details': proc
                    })
                    continue

                # 4. Check Suspicious Locations (e.g., executing from /tmp)
                if exe and ('/tmp' in exe or '/dev/shm' in exe):
                    suspicious_list.append({
                        'pid': pid,
                        'name': name,
                        'reason': f"Executing from suspicious directory: {exe}",
                        'details': proc
                    })
                    continue

            except Exception as e:
                self.logger.error(f"Error analyzing process {proc.get('pid', '?')}: {e}")

        return suspicious_list
