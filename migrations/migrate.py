import logging
import subprocess

logger = logging.getLogger(__name__)

def run_migration(downgrade=False):
    if downgrade:
        subprocess.run(["alembic", "downgrade", "-1"], check=True)
    else:
        logger.info("Running alembic upgrade")
        subprocess.run(["alembic", "upgrade", "head"], check=True)