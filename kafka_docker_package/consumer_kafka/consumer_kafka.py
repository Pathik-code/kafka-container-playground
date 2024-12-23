import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kafka_configuration import KafkaConsumerClient, bootstrap_servers, TOPICS
import json

# Initialize the Kafka consumer
consumer = KafkaConsumerClient(TOPICS[0], bootstrap_servers)

# Data storage for live graph
data = []

# Function to update the graph
def update_graph(i):
    global data
    plt.cla()  # Clear the current axes
    plt.plot(data, label='Account Balance')
    plt.xlabel('Time')
    plt.ylabel('Account Balance')
    plt.title('Live Account Balance Data')
    plt.legend(loc='upper left')

# Function to consume messages and update data
def consume_messages():
    global data
    for message in consumer.consumer:
        message_value = json.loads(message.value)
        account_balance = message_value.get('AccountBalance', 0)
        data.append(account_balance)
        if len(data) > 100:  # Keep only the last 100 data points
            data.pop(0)

# Main execution
if __name__ == "__main__":
    # Start the consumer in a separate thread
    import threading
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    # Set up the live graph
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update_graph, interval=1000)
    plt.show()

    # Close the consumer after the graph is closed
    consumer.consumer.close()
