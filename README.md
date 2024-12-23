```mermaid
# Real-Time Trading Data Streaming System

## Purpose
This project implements a sophisticated real-time data streaming pipeline that:
- Generates synthetic trading user data including user profiles, trading preferences, and account details
- Leverages Apache Kafka for reliable, scalable data streaming
- Persists data in PostgreSQL for historical analysis
- Provides real-time data visualization through dynamic dashboards
- Demonstrates event-driven architecture principles
- Showcases containerized microservices deployment

### Key Features
1. Data Generation
   - Synthetic user profiles with realistic attributes
   - Random trading categories and experience levels
   - Simulated account balances and transaction data
   - Configurable data generation parameters

2. Kafka Implementation
   - Multi-topic architecture for different data streams
   - Scalable producer-consumer pattern
   - Fault-tolerant message delivery
   - Real-time data processing capabilities

3. Data Persistence
   - Structured PostgreSQL schema design
   - Efficient bulk data loading
   - Data integrity and consistency checks
   - Query optimization for analytics

4. Visualization
   - Real-time data plotting
   - Interactive dashboards
   - Performance metrics monitoring
   - Custom analytics views

### Technical Stack
- Apache Kafka for event streaming
- PostgreSQL for data storage
- Python with Pandas for data processing
- Docker for containerization
- Matplotlib/Plotly for visualization

## System Architecture

The system follows a microservices architecture pattern with containerized services communicating through Apache Kafka. The architecture consists of the following key components:

### Core Components
1. **Data Generation Service**
   - Generates synthetic trading data
   - Implements configurable data generation rates
   - Produces data in JSON format
   - Handles multiple data types (user profiles, trades, market data)

2. **Kafka Cluster**
   - Broker node running on port 9092
   - Topic partitioning for parallel processing
   - Message retention policies for data persistence

3. **Consumer Services**
   - Multiple consumer groups for different data processing needs
   - Stateless processing nodes for scalability
   - Error handling and dead letter queues
   - Message acknowledgment mechanisms

4. **PostgreSQL Database**
   - Normalized schema for user and trading data
   - Partitioned tables for efficient querying
   - Indexes optimized for common query patterns
   - Connection pooling for better performance

### Data Flow
1. **Data Generation → Kafka**
   - JSON messages sent to specific topics
   - Configurable batch sizes and compression
   - Built-in retry mechanisms
   
2. **Kafka → Consumers**
   - At-least-once delivery guarantee
   - Consumer group load balancing
   - Parallel message processing
   
3. **Consumers → PostgreSQL**
   - Bulk insert operations
   - Transaction management
   - Data validation and transformation

### High Availability Features
- Kafka replication factor: 3 (configurable)
- Consumer group failover
- Database replication options
- Container orchestration with Docker Compose

### Monitoring Points
- Kafka metrics (throughput, latency)
- Consumer lag monitoring
- Database performance metrics
- System resource utilization

### Security Measures
- SSL/TLS encryption for Kafka
- Database access control
- Network isolation
- Authentication mechanisms

### Console Diagram
```mermaid
sequenceDiagram
    participant DG as Data Generator
    participant KB as Kafka Broker
    participant DC as Data Consumer
    participant DB as PostgreSQL
    participant VZ as Visualizer

    DG->>KB: Send User Data
    DG->>KB: Send Stock Data
    KB->>DC: Consume Messages
    DC->>DB: Store Data
    DC->>VZ: Stream Data
    VZ->>VZ: Update Visualization

### Project Startup Guide
    1. Environment Setup
        # Create virtual environment
        python -m venv venv
        source venv/bin/activate

        # Install dependencies
        pip install -r requirements.txt
    2. Start Kafka Container
        # Start Kafka and create network
        docker network create kafka-network
        docker-compose up -d
    3. Create Kafka Topics
        # Run topic creation script
        python create_topics.py
    3. Start Data Generation
        # Terminal 1: User Data Generator
        python user_data_generator.py

        # Terminal 2: Stock Data Generator
        python stock_price_generator.py
    4. Start Consumer Services
        # Terminal 3: Data Consumer & PostgreSQL
        python consumer_user_data.py

        # Terminal 4: Visualization
        python consumer_data_visualization.py
    5. Monitor Data Flow
        # Check Kafka logs
        docker-compose logs -f kafka

        # Check Consumer Group Status
        docker exec kafka kafka-consumer-groups \
            --bootstrap-server localhost:9092 \
            --describe --group consumer-group-1
    6. shutdown
        # Stop Kafka and remove containers
        docker-compose down
        # Deactivate virtual environment
        deactivate

### Directory Structure
kafka-container-test/
├── kafka_docker_package/
│   ├── producer_kafka/
│   │   ├── create_topics.py
│   │   ├── kafka_configuration.py
│   │   ├── stock_price_generator.py
│   │   └── user_data_generator.py
│   ├── consumer_kafka/
│   │   ├── consumer_user_data.py
│   │   ├── consumer_data_visualization.py
│   │   ├── test_consumer.py
│   │   └── consumer_stock_data.py
├── docker-compose.yml
├── Dockerfile
└── README.md



### Important Notes

#### Prerequisites
- This project is for educational purposes only
- Ensure you have installed:
  - Docker and Docker Desktop
  - Python 3.8+
  - PostgreSQL
  - Required Python packages (`requirements.txt`)

#### Setup & Execution Steps
1. **Docker Setup**
   ```bash
   # Start Docker daemon
   sudo systemctl start docker
   
   # Verify Docker is running
   docker --version

2. **Start Services**
   ```bash
    # Build and start containers
    docker-compose up -d

3. **Database Setup**
    ```bash
    # Initialize PostgreSQL
    docker exec -it postgres psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/init.sql
4. **Run Components**
    ```bash
    # Start data generators
    python kafka_docker_package/producer_kafka/user_generator.py
    python kafka_docker_package/producer_kafka/trading_generator.py

    # Start consumers with visualization
    python kafka_docker_package/consumer_kafka/visualization_consumer.py

### Conclusion
## This project demonstrates a real-time data processing pipeline using:
    - Apache Kafka for message streaming
    - PostgreSQL for data persistence
    - Python for data generation and processing
    - Matplotlib for real-time visualization
    - Docker for containerized deployment                     
## The system architecture showcases:
    - Scalable message processing
    - Real-time data visualization
    - Persistent data storage
    - Containerized deployment
    - For issues, improvements, or questions, please create an issue in the repository.

Happy Learning! 🚀 

## Frequently Asked Questions (FAQ)

### Q1: How do I troubleshoot Kafka connection issues?
**A:** Common steps to resolve Kafka connection issues:
1. Verify Kafka container is running: `docker ps`
2. Check Kafka logs: `docker-compose logs kafka`
3. Ensure correct port mapping (default 9092)
4. Verify network connectivity: `docker network inspect kafka-network`

### Q2: Why is my data generator not producing messages?
**A:** Common causes and solutions:
1. Check Kafka topic exists: `docker exec kafka kafka-topics --list --bootstrap-server localhost:9092`
2. Verify producer configurations in `kafka_configuration.py`
3. Ensure proper Python environment activation
4. Check for any error messages in the producer logs

### Q3: How can I scale the consumer services?
**A:** To scale consumers:
1. Increase topic partitions:

### Q4: How do I monitor system performance?
**A:** Available monitoring options:
1. Kafka Manager UI (CMAK) for broker monitoring
2. Consumer group lag: `kafka-consumer-groups` command
3. PostgreSQL metrics through pg_stat views
4. Docker stats: `docker stats`

### Q5: What should I do if data visualization is not updating?
**A:** Troubleshooting steps:
1. Verify consumer is receiving messages
2. Check matplotlib/plotly configuration
3. Ensure proper data format in visualization consumer
4. Monitor system resources for bottlenecks

### Q6: How can I modify the data generation parameters?
**A:** Customize data generation by:
1. Editing configuration in producer scripts
2. Adjusting generation frequency
3. Modifying data schemas
4. Adding new data fields

### Q7: How can I implement custom data transformations?
**A:** To implement custom transformations:
1. Create a new transformer class in the consumer package
2. Implement the transformation logic
3. Add configuration parameters as needed
4. Update the consumer to use the new transformer

### Q8: What's the recommended way to handle schema changes?
**A:** Best practices for schema evolution:
1. Use schema versioning in Kafka messages
2. Implement backward compatible changes
3. Update PostgreSQL schema using migrations
4. Test compatibility with existing consumers
5. Document schema changes in version control

### Q9: How can I optimize Kafka performance?
**A:** Key optimization strategies:
1. Adjust batch size and linger.ms settings
2. Configure appropriate partition count
3. Tune JVM parameters for broker
4. Monitor and adjust compression settings
5. Implement proper message key distribution

### Q10: How do I backup and restore the system?
**A:** Backup procedures:
1. Kafka topics backup:

### Q11: How do I implement custom data transformations?
**A:** Implement transformations by:
```python
# In consumer/processor.py
def transform_data(message):
    try:
        # Parse message
        data = json.loads(message)
        
        # Apply transformations
        transformed = {
            'timestamp': datetime.now(),
            'user_id': data['user_id'],
            'amount': round(float(data['amount']), 2),
            'category': data['category'].upper()
        }
        return transformed
    except Exception as e:
        logger.error(f"Transform error: {e}")
        return None

### Q12: How do I process real-time trading data?
**A:** Here's a complete example of processing trading data:

```python
# trading_processor.py
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class TradingDataProcessor:
    def __init__(self):
        self.processed_count = 0
        
    def process_trade(self, message):
        try:
            # Parse trading data
            trade_data = json.loads(message)
            
            # Transform and validate
            processed_trade = {
                'trade_id': trade_data.get('trade_id'),
                'timestamp': datetime.now().isoformat(),
                'symbol': trade_data['symbol'].upper(),
                'price': round(float(trade_data['price']), 2),
                'quantity': int(trade_data['quantity']),
                'trade_type': trade_data['type'].upper(),
                'processed': True
            }
            
            self.processed_count += 1
            logger.info(f"Processed trade {processed_trade['trade_id']}")
            return processed_trade
            
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return None
        except ValueError as e:
            logger.error(f"Invalid data format: {e}")
            return None
        except Exception as e:
            logger.error(f"Processing error: {e}")
            return None

# Usage Example:
processor = TradingDataProcessor()
trade_message = '''
{
    "trade_id": "T123",
    "symbol": "AAPL", 
    "price": "150.25",
    "quantity": "100",
    "type": "buy"
}
'''
result = processor.process_trade(trade_message)


### Q13: How do I implement a real-time price alerting system?
**A:** Here's an implementation of a price alert system:

```python
# price_alerter.py
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class PriceAlertSystem:
    def __init__(self):
        self.price_alerts = {}  # symbol -> alert_price mapping
        
    def set_alert(self, symbol: str, target_price: float):
        self.price_alerts[symbol] = target_price
        logger.info(f"Alert set for {symbol} at {target_price}")
        
    def check_price(self, message: str) -> dict:
        try:
            price_data = json.loads(message)
            symbol = price_data['symbol'].upper()
            current_price = float(price_data['price'])
            
            if symbol in self.price_alerts:
                target_price = self.price_alerts[symbol]
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'current_price': current_price,
                    'target_price': target_price,
                    'triggered': current_price >= target_price
                }
                return alert
                
        except Exception as e:
            logger.error(f"Alert processing error: {e}")
        return None

# Usage Example:
alerter = PriceAlertSystem()
alerter.set_alert("AAPL", 150.00)
price_update = '{"symbol": "AAPL", "price": "151.25"}'
alert = alerter.check_price(price_update)