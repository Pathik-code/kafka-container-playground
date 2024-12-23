from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeVisualizer:
    def __init__(self, max_points=10):
        self.consumer = KafkaConsumer(
            'user-data',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest'
        )
        
        self.users = deque(maxlen=max_points)
        self.balances = deque(maxlen=max_points)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        
    def update_plot(self, frame):
        try:
            # Get messages without blocking
            messages = self.consumer.poll(timeout_ms=100)
            
            for message_set in messages.values():
                for message in message_set:
                    data = message.value
                    self.users.append(data.get('UserID', 'Unknown'))
                    self.balances.append(float(data.get('AccountBalance', 0)))
                    logger.info(f"Received data: {data}")
            
            # Clear and redraw
            self.ax.clear()
            if self.users and self.balances:
                self.ax.bar(list(self.users), list(self.balances))
                self.ax.set_xticklabels(self.users, rotation=45, ha='right')
                self.ax.set_ylabel('Account Balance ($)')
                self.ax.set_title('Live Trading Account Balances')
                plt.tight_layout()
                
        except Exception as e:
            logger.error(f"Error in update_plot: {e}")
    
    def start(self):
        try:
            logger.info("Starting visualization...")
            ani = FuncAnimation(
                self.fig, 
                self.update_plot,
                interval=1000,
                cache_frame_data=False
            )
            plt.show()
        except KeyboardInterrupt:
            logger.info("Visualization stopped by user")
        finally:
            self.consumer.close()
            
if __name__ == "__main__":
    visualizer = RealTimeVisualizer()
    visualizer.start()
