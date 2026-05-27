import logging
import os


# ==========================================
# Create logs folder if not exists
# ==========================================

os.makedirs(
    "logs",
    exist_ok=True
)


# ==========================================
# Logging Configuration
# ==========================================

logging.basicConfig(

    filename="logs/app.log",

    level=logging.INFO,

    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


# ==========================================
# Logger Object
# ==========================================

logger = logging.getLogger()