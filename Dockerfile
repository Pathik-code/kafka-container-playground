FROM confluentinc/cp-kafka:7.4.0

RUN mkdir -p /var/lib/kafka/data

EXPOSE 9092 29093

VOLUME ["/var/lib/kafka/data"]

CMD ["sh", "-c", "kafka-storage format -t $(kafka-storage random-uuid) -c /etc/kafka/kraft/server.properties && kafka-server-start /etc/kafka/kraft/server.properties"]