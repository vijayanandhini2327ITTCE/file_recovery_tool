# forensic_recovery_tool/utils.py

import hashlib
import logging
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_sha256(file_path):
    """
    Generates the SHA-256 hash of a file.
    """
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error generating hash for {file_path}: {e}")
        return None

def log_carving_activity(message):
    """
    Logs a message with a timestamp.
    """
    logging.info(message)

def get_timestamp():
    """
    Returns the current timestamp string.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Example usage (will not run in the web app context, just for completeness)
if __name__ == '__main__':
    # This part is just for testing the utility functions locally
    # In the actual application, these functions will be imported and used.
    log_carving_activity("Utility module loaded.")
    print(f"Current timestamp: {get_timestamp()}")
