import json
import sys
import six
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
# from kafka import KafkaConsumer
import logging
from kafka_configuration import KafkaConsumerClient, bootstrap_servers, TOPICS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


KAFKA_BROKER = bootstrap_servers
TOPIC = 'user-data'


consumer_obj = KafkaConsumerClient(TOPIC, KAFKA_BROKER)

consumer_obj.consume_messages()

