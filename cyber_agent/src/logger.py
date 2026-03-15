import logging
import sys
import os

def setup_logging(config):
    """
    Configures logging based on the provided configuration.
    """
    log_level_str = config['agent'].get('log_level', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    log_file = config['agent'].get('log_file', '/var/log/cyber-agent.log')
    
    # Create logger
    logger = logging.getLogger("CyberAgent")
    logger.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console Handler (Stdout)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File Handler
    # Only add file handler if we can write to the location (might fail on Windows without admin)
    try:
        # distinct logic for windows dev vs linux prod
        if os.name == 'nt':
            # For Windows development, log to a local file instead of /var/log
            log_file = "cyber-agent.log"
            
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not setup file logging to {log_file}: {e}")
        
    return logger
