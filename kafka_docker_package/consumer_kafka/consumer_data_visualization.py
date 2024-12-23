from kafka_configuration import KafkaConsumerClient, bootstrap_servers
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import threading
import queue
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaDataVisualizer:
    def __init__(self, topic):
        self.consumer = KafkaConsumerClient('user-data', bootstrap_servers)
        self.data_queue = queue.Queue(maxsize=100)
        self.df = pd.DataFrame(columns=['UserID', 'Name', 'AccountBalance'])
        
    def consume_data(self):
        try:
            for data in self.consumer.consume_messages():
                if isinstance(data, dict):
                    if len(self.df) >= 10:
                        self.df = self.df.iloc[1:]
                    new_row = pd.DataFrame([{
                        'UserID': data.get('UserID', 'Unknown'),
                        'Name': data.get('Name', 'Anonymous'),
                        'AccountBalance': data.get('AccountBalance', 0)
                    }])
                    self.df = pd.concat([self.df, new_row], ignore_index=True)
                    self.data_queue.put(self.df.copy())
        except Exception as e:
            logger.error(f"Error consuming data: {e}")
            
    def update_plot(self, frame):
        try:
            if not self.data_queue.empty():
                df = self.data_queue.get()
                plt.cla()
                bars = plt.bar(df['Name'], df['AccountBalance'])
                plt.xticks(rotation=45, ha='right')
                plt.xlabel('Name')
                plt.ylabel('Account Balance')
                plt.title('Live Trading Account Balances')
                
                # Add UserID as text on top of bars
                for bar in bars:
                    height = bar.get_height()
                    idx = bars.patches.index(bar)
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'${height:,.0f}',
                            ha='center', va='bottom')
                
                plt.tight_layout()
        except Exception as e:
            logger.error(f"Error updating plot: {e}")

    def start_visualization(self):
        # Start consumer thread
        consumer_thread = threading.Thread(target=self.consume_data, daemon=True)
        consumer_thread.start()

        # Create animation
        fig = plt.figure(figsize=(10, 6))
        ani = FuncAnimation(fig, self.update_plot, interval=1000)
        plt.show()

if __name__ == "__main__":
    visualizer = KafkaDataVisualizer("user-data")
    visualizer.start_visualization()
