import logging


def generate_logger():
    FORMAT = "[%(levelname)s] %(name)s:%(lineno)d : %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
