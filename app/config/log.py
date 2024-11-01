import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: [%(asctime)s] %(name)s - %(message)s',
)

logger = logging.getLogger(__name__)