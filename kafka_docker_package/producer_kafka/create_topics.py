import subprocess
from kafka_configuration import TOPICS, bootstrap_servers, TopicCreation # Import topics from kafka_configuration.py
# Kafka broker details
KAFKA_BROKER = bootstrap_servers


# Function to create Kafka topics
def create_kafka_topics(broker, topics):
    for topic in topics:
        try:
            # Initialize the TopicCreation class
            topic_creation = TopicCreation(broker)

            # Create the topic
            result = topic_creation.create_topic(topic, 1, 1)

            print(f"Topic '{topic}' created successfully.")
            # print(result)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error creating topic '{topic}': {e.stderr}")

# Main execution
if __name__ == "__main__":
    create_kafka_topics(KAFKA_BROKER, TOPICS)
