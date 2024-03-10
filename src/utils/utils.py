import os
import yaml
import logging
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def load_config(config_name):
    logger.info("Loading Config File")
    with open(os.path.join(config_name)) as file:
        config = yaml.safe_load(file)
    return config
