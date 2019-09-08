import os
import sys
sys.path.extend(["lib/"+x for x in os.listdir("lib") if x.endswith('.jar')])
sys.path.extend(["dist/"+x for x in os.listdir("dist") if x.endswith('.jar')])

import jarray
from kafka.api import FetchRequest
from kafka.consumer import SimpleConsumer

consumer = SimpleConsumer("localhost", 9092, 10000, 1024000)
req = FetchRequest("test", 0, 0, 1000000)
messageset = consumer.fetch(req) # ByteBufferMessageSet

msgs = list(messageset.elements()) # [kafka.message.Message]
for msg in msgs:
    buf = msg.payload() # java.nio.HeapByteBuffer
    barray = jarray.zeros(buf.remaining(), 'b')
    buf.get(barray)
    print barray.tostring()
