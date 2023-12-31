import pytest
from unittest.mock import patch
from your_module_path.kafka import produce_message, consume_messages

# Replace 'your_module_path' with the actual path where your kafka.py module is located

@pytest.mark.parametrize("message", ["Test message 1", "Test message 2", "Test message 3"])
def test_produce_and_consume(message):
    kafka_topic = "test_topic"

    # Test produce_message
    with patch("your_module_path.kafka.Producer") as mock_producer:
        produce_message(kafka_topic, message)
        mock_producer.return_value.produce.assert_called_once_with(kafka_topic, value=message)
        mock_producer.return_value.flush.assert_called_once()

    # Test consume_messages
    with patch("your_module_path.kafka.Consumer") as mock_consumer:
        mock_poll = mock_consumer.return_value.poll
        mock_poll.return_value.error.return_value = None
        mock_poll.return_value.value.return_value = message.encode('utf-8')

        consume_messages(kafka_topic)

        mock_consumer.assert_called_once_with({
            'bootstrap.servers': 'your_kafka_bootstrap_servers',
            'group.id': 'kafka_consumer_example',
            'auto.offset.reset': 'earliest'
        })
        mock_consumer.return_value.subscribe.assert_called_once_with([kafka_topic])
        mock_poll.assert_called_once_with(1.0)
        assert mock_poll.return_value.value.call_count == 1

# Add more test cases as needed
