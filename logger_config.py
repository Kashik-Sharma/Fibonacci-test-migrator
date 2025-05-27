import logging
import os

# Configure logger
log_file_path = os.path.join(os.path.dirname(__file__), 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Log to file
        logging.StreamHandler()             # Log to console
    ]
)

logger = logging.getLogger(__name__)
