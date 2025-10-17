import zmq
import sys
import time

global QUIT
QUIT = False

port = "5559"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:%s" % port)


product_listings = {
    ("SnowMobile", 75),
    ("SnowPants", 20),
    ("SnowBlower", 45)
}

while not QUIT:
    try:
        for product_info in product_listings:
            print("Item: %s | Stock: %d" % product_info)
            socket.send_string("%s %d" % product_info)
            time.sleep(1)
            
        time.sleep(5)
    except KeyboardInterrupt:
        QUIT = True
        print("\nInterrupted, shutting down publisher...")