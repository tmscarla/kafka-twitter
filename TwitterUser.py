
# CONSTANTS
KEY_SCHEMA = 'key_schema.avsc'
VALUE_SCHEMA = 'tweet_schema.avsc'

TOPIC = 'start5'

BOOTSTRAP_SERVERS = 'localhost:9092'
SCHEMA_REGISTRY_URL = 'http://127.0.0.1:8081'

class TwitterUser:
    def __init__(self, id):
        # the ID
        self.id = id
        # the Avro Schemas
        self.key_schema = avro.loads(open(KEY_SCHEMA, 'r', newline='').read())
        self.value_schema = avro.loads(open(VALUE_SCHEMA, 'r', newline='').read())

        # create consumer and producer
        # Avro Consumer
        self.c = AvroConsumer(
            {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': f'{id}',
            'schema.registry.url': SCHEMA_REGISTRY_URL
            }
        )
        # assign the partition
        self.c.assign([TopicPartition(TOPIC, 0,0)])

        # create producer
        self.p = AvroProducer(
            {
            'bootstrap.servers': 'localhost:9092',
            'schema.registry.url': 'http://127.0.0.1:8081'
            }, default_key_schema=key_schema, default_value_schema=value_schema
        )
