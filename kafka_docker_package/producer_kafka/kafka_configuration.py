# kafka_package/kafka_configuration.py
import json
import logging
import sys
import six
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient as AdminClient
from kafka.admin import NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bootstrap_servers = 'localhost:9092'

TOPICS = ["user-data", "stock-data"]

class TopicCreation:
    def __init__(self, bootstrap_servers):
        self.admin_client = AdminClient(bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        try:
            self.admin_client.create_topics(new_topics=topic_list)
            logging.info(f"Topic {topic_name} created successfully")
            return self.admin_client  # Return the admin client connection
        except TopicAlreadyExistsError:
            logging.info(f"Topic {topic_name} already exists")
            return self.admin_client  # Return the admin client connection
        except KafkaError as e:
            logging.error(f"Failed to create topic: {e}")
            raise

    def close(self):
        self.admin_client.close()

class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_message(self, topic, message):
        try:
            self.producer.send(topic, message)
            self.producer.flush()
            logger.info(f"Message sent to topic {topic}: {message}")
            return self.producer  # Return the producer connection
        except KafkaError as e:
            logger.error(f"Failed to produce message: {e}")
            raise

    def close(self):
        self.producer.close()

class KafkaConsumerClient:
    def __init__(self, topic_name, bootstrap_servers):
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: self.try_decode(x)
        )

    def consume_messages(self):
        try:
            for message in self.consumer:
                logger.info(f"Received message: {message.value}")
            return self.consumer  # Return the consumer connection
        except KafkaError as e:
            logger.error(f"Failed to consume messages: {e}")
            raise
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
        finally:
            self.consumer.close()

    @staticmethod
    def try_decode(message):
        try:
            return json.loads(message.decode('utf-8'))
        except json.JSONDecodeError:
            return message.decode('utf-8')

class KafkaAdminClient:
    def __init__(self, bootstrap_servers):
        self.admin_client = AdminClient(bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        try:
            self.admin_client.create_topics(new_topics=topic_list)
            logger.info(f"Topic {topic_name} created successfully")
            # return self.admin_client
        except TopicAlreadyExistsError:
            logger.info(f"Topic {topic_name} already exists")
            # return self.admin_client
        except KafkaError as e:
            logger.error(f"Failed to create topic: {e}")
            raise

    def close(self):
        self.admin_client.close()

# # Example usage
# if __name__ == "__main__":
#     bootstrap_servers = 'localhost:9092'
#     topic_name = 'test_topic'
#     message = {'key': 'value'}

#     # Create topic and get admin client connection
#     topic_creator = TopicCreation(bootstrap_servers)
#     admin_client = topic_creator.create_topic(topic_name)
#     topic_creator.close()

#     # Produce message and get producer connection
#     producer = KafkaProducerClient(bootstrap_servers)
#     producer_connection = producer.produce_message(topic_name, message)
#     producer.close()

#     # Consume messages and get consumer connection
#     consumer = KafkaConsumerClient(topic_name, bootstrap_servers)
#     consumer_connection = consumer.consume_messages()

