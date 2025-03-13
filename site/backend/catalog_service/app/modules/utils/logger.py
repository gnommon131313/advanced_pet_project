import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Просто показ логов с уровнем INFO и выше
logger = logging.getLogger(__name__)