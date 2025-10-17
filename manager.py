import sys
import zmq
import time

# set up broker

subport = "5559" # port for proxy frontend socket
pubport = "5560" # port for proxy backend socket

if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context(1)

#####################
# zmq.PROXY sockets #
#####################

# subsocket = context.socket(zmq.XSUB)
# subsocket.bind("tcp://*:%s" % subport)

# #subsocket.setsockopt_string(zmq.SUBSCRIBE, "")

# pubsocket = context.socket(zmq.XPUB)
# pubsocket.bind("tcp://*:%s" % pubport)

# print("Running Proxy...")
# try:
#     time.sleep(1)
#     zmq.proxy(subsocket, pubsocket)
# except KeyboardInterrupt:
#     print("\nInterrupted. Shutting down proxy")

#######################################################

######################
# zmq.poller sockets #
######################

subsocket = context.socket(zmq.SUB)
subsocket.bind("tcp://*:%s" % subport)

subsocket.setsockopt_string(zmq.SUBSCRIBE, "")

pubsocket = context.socket(zmq.PUB)
pubsocket.bind("tcp://*:%s" % pubport)

cache = {}

poller = zmq.Poller()
poller.register(subsocket, zmq.POLLIN)
poller.register(pubsocket, zmq.POLLIN)
while True:

    try:
        events = dict(poller.poll(1000))
    except KeyboardInterrupt:
        print("\nInterrupted")
        break

    # Any new topic data we cache and then forward
    if subsocket in events:
        string = subsocket.recv_string()
        topic, message = string.split()
        cache[topic] = message
        pubsocket.send_string(string)

    # handle subscriptions
    # When we get a new subscription we pull data from the cache:
    if pubsocket in events:
        event = pubsocket.recv()
        # Event is one byte 0=unsub or 1=sub, followed by topic
        if event[0] == 1:
            topic = event[1:]
            if topic in cache:
                print("Sending cached topic %s" % topic)
                pubsocket.send_string([ topic, cache[topic] ])
        elif event[0] == 0:
            topic 
