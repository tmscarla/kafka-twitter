import os
import appscript
import time

PATH_TO_CONFLUENT_DIR = '/Documents/GitHub/kafka-twitter' # CHANGE THIS

# commands to run kafka
run_zk = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/bin/zookeeper-server-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/etc/kafka/zookeeper.properties"
run_kafka = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/bin/kafka-server-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/etc/kafka/server.properties"
run_schema_reg = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/bin/schema-registry-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/etc/schema-registry/schema-registry.properties"
run_rest = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/bin/kafka-rest-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.1.2/etc/kafka-rest/kafka-rest.properties"

# execute shell commands
cl = appscript.app('Terminal')

cl.do_script(run_zk)
time.sleep(4)
cl.do_script(run_kafka)
time.sleep(4)
cl.do_script(run_rest)
time.sleep(8)
cl.do_script(run_schema_reg)