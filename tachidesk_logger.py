import logging


def get_logger():
    logging.basicConfig(filename=f'/home/nishant/tachidesk/tachidesk-scripts/tachidesk_log.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level='INFO')

    logger = logging.getLogger()
    return logger
