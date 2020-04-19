import logging

from actions.user import ProfileAction
from data_store import utils

logger = logging.getLogger(__name__)
# create console handler and set level to debug
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
if __name__ == '__main__':
    consumer = utils.get_consumer()

    for message in consumer:
        action = ProfileAction(
            action_name=message.key.decode('utf-8'),
            data=message.value,
        )
        action.run()
        logger.info(
            "%s:%d:%d: key=%s value=%s",
            message.topic,
            message.partition,
            message.offset,
            message.key,
            message.value,
        )
