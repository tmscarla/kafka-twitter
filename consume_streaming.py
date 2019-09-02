from confluent_kafka import Consumer, KafkaError

# Set 'auto.offset.reset': 'smallest' if you want to consume all messages
# from the beginning of the topic the first time that this runs.
#
# If you want to monitor your data streams through Confluent Control Center,
# make sure you've installed the interceptors and then uncomment
# the 'plugin.library.paths' config line
# Ref: https://docs.confluent.io/current/control-center/docs/installation/clients.html#installing-control-center-interceptors
settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'scemo',
#    'plugin.library.paths': 'monitoring-interceptor',
    'default.topic.config': {'auto.offset.reset': 'earliest'}
}
c = Consumer(settings)

c.subscribe(['prova_4'])


try:
    while True:
        msg = c.poll()

        if msg is None:
            continue

        elif not msg.error():
            print('Received message: {0}'.format(msg.value()))

            if msg.value() is None:
                continue

            # Handle UTF
            try:
                data = msg.value().decode()
            except Exception:
                data = msg.value()

            # Try to parse the message as JSON
            try:
                app_msg = json.loads(data)
            except Exception:
                print('Could not parse JSON, will just use raw message contents')
                app_msg = data

            # Try to extract the channel & message
            try:
                channel=app_msg['CHANNEL']
                text=app_msg['TEXT']
            except Exception:
                print('Failed to get channel/text from message')
                channel='general'
                text=msg.value()

            print('\nSending message "{}" to channel {}'.format(channel, text))

        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {}/{}'
                  .format(msg.topic(), msg.partition()))

        else:
            print('Error occured: {}'.format(msg.error()))

except Exception as e:
    print(e)

finally:
    c.close()
