import matplotlib
matplotlib.use('TkAgg')
from kafka_configuration import KafkaConsumerClient
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import threading
import logging
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccountBalanceVisualizer:
    def __init__(self):
        self.consumer = KafkaConsumerClient('user-data', ['localhost:9092'])
        self.start_time = datetime.now()
        self.data_df = pd.DataFrame(columns=['Seconds', 'TotalBalance'])
        self.data_df['TotalBalance'] = self.data_df['TotalBalance'].astype(float)
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.setup_plot()
        
    def setup_plot(self):
        self.ax.set_title('Cumulative Account Balance Over Time')
        self.ax.set_xlabel('Seconds Elapsed')
        self.ax.set_ylabel('Total Balance ($)')
        self.ax.grid(True)
        
    def update_plot(self, frame):
        try:
            self.ax.clear()
            self.setup_plot()
            
            if not self.data_df.empty:
                self.ax.plot(self.data_df['Seconds'], self.data_df['TotalBalance'], 'b-', label='Total Balance')
                max_val = self.data_df['TotalBalance'].max()
                self.ax.set_ylim(0, max_val * 1.1 if max_val > 0 else 100)
                # Keep x-axis showing last 60 seconds
                current_time = (datetime.now() - self.start_time).total_seconds()
                self.ax.set_xlim(max(0, current_time - 60), current_time)
                
            self.ax.legend()
            plt.tight_layout()
        except Exception as e:
            logger.error(f"Error updating plot: {e}")

    def consume_messages(self):
        try:
            total_balance = 0
            for message in self.consumer.consume_messages():
                current_seconds = (datetime.now() - self.start_time).total_seconds()
                account_balance = float(message.get('AccountBalance', 0))
                total_balance += account_balance
                
                new_row = pd.DataFrame([{
                    'Seconds': current_seconds,
                    'TotalBalance': total_balance
                }])
                
                self.data_df = pd.concat([self.data_df, new_row], ignore_index=True)
                
                # Keep only data points from the last 60 seconds
                cutoff_time = current_seconds - 60
                self.data_df = self.data_df[self.data_df['Seconds'] > cutoff_time]
                
                logger.info(f"Time: {current_seconds:.1f}s, Total Balance: ${total_balance:,.2f}")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")

    def start_visualization(self):
        try:
            # Start consumer thread
            consumer_thread = threading.Thread(target=self.consume_messages, daemon=True)
            consumer_thread.start()

            # Create animation
            ani = animation.FuncAnimation(
                self.fig,
                self.update_plot,
                interval=1000,
                cache_frame_data=False,
                save_count=100
            )
            
            plt.show()
        except Exception as e:
            logger.error(f"Error in visualization: {e}")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    try:
        visualizer = AccountBalanceVisualizer()
        visualizer.start_visualization()
    except KeyboardInterrupt:
        logger.info("Visualization stopped by user")