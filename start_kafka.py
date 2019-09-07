import os
import appscript
import time

PATH_TO_CONFLUENT_DIR = '/Documents/GitHub/kafka-twitter' # CHANGE THIS

# commands to run kafka
run_zk = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/bin/zookeeper-server-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/etc/kafka/zookeeper.properties"
run_kafka = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/bin/kafka-server-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/etc/kafka/server.properties"
run_schema_reg = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/bin/schema-registry-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/etc/schema-registry/schema-registry.properties"
run_rest = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/bin/kafka-rest-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/etc/kafka-rest/kafka-rest.properties"

run_ksql = f".{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/bin/ksql-server-start .{PATH_TO_CONFLUENT_DIR}/confluent-5.3.0/etc/ksql/ksql-server.properties"

#/Users/Teo/Documents/GitHub/kafka-twitter/confluent-5.3.0/bin/ksql-server-start /Users/Teo/Documents/GitHub/kafka-twitter/confluent-5.3.0/etc/ksql/ksql-server.properties

# execute shell commands
cl = appscript.app('Terminal')

cl.do_script(run_zk)
time.sleep(4)
cl.do_script(run_kafka)
time.sleep(4)
cl.do_script(run_rest)
time.sleep(8)
cl.do_script(run_schema_reg)
time.sleep(4)
cl.do_script(run_ksql)
