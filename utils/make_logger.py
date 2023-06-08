import logging

def make_logger() -> logging.Logger:
    logger = logging.Logger('global_logger')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger