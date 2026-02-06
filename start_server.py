import logging
import sys
from pathlib import Path

# Add the current directory to sys.path to ensure lexicard package is found
sys.path.append(str(Path.cwd()))

logging.basicConfig(level=logging.DEBUG, filename="server.log", filemode="w")
logger = logging.getLogger(__name__)

try:
    logger.info("Starting Lexicard server...")
    from lexicard.main import main
    main()
except Exception as e:
    logger.exception("Failed to start server")
    raise
