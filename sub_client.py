import sys
import zmq

global QUIT 
QUIT = False

port = "5560"

user_input = ""
product_filter = ""

# Socket to talk to backend of manager

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Connecting to proxy server...")
socket.connect("tcp://localhost:%s" % port)

socket.setsockopt(zmq.RCVTIMEO, 10000)

while (not QUIT):

    user_input = input("Select an option:\n[1] Check available items\n[2] Purchase Item\n[3] Quit the program\n>>> ")

    if (user_input == "1"):
        socket.setsockopt_string(zmq.SUBSCRIBE, "")

        update_nbr = 3

        for i in range(update_nbr):
            try:
                string = socket.recv()
            except Exception as e:
                print("Timing out...")
                break

            topic, messagedata = string.split()
            print("%s %s" % (topic, messagedata))
        socket.unsubscribe("")
        continue

    elif (user_input == "2"):

        user_input = input("Enter your desired product, or type \"quit\" to go back: ")

        # QUIT quits, <productname> searches for product of that name, redoes input prompt

        if (user_input.lower() == "quit"):
            print("Returning to option select...")
            continue

        product_filter = user_input

        socket.setsockopt_string(zmq.SUBSCRIBE, product_filter)

        try:
            string = socket.recv()
        except Exception as e:
            print(e)
            socket.unsubscribe(product_filter)
            continue

        topic, messagedata = string.split()
        
        print("Item: %s | Stock : %s" % (topic, messagedata))

        user_input = input("Would you like to purchase some? [Y/n]: ")

        while (user_input.lower() != "y" and user_input.lower() != "n"):
            print("Enter either \"Y\" or \"n\":")
            user_input = input("Would you like to purchase some? [Y/n]: ")
        
        if (user_input.lower() == "y"):
            msgtopic = "buying"
            user_input = input("How much?: ")
            

            if (int(user_input) > int(messagedata.decode())):
                print("Not enough in stock.")
                user_input = ""
            
            elif (int(user_input) < 0):
                print("Number cannot be negative")
                user_input = ""
                

            while (not user_input.isdigit()):
                user_input = input("Please enter a numerical amount: ")
                if (int(user_input) > int(messagedata.decode())):
                    print("Not enough in stock.")
                    user_input = ""

                elif (int(user_input) < 0):
                    print("Number cannot be negative")
                    user_input = ""

            print("Item purchased.")

        socket.unsubscribe(topic)

    elif (user_input == "3"):
        QUIT = True
        print("Quitting application...")
        continue

    else:
        print("Please enter 1, 2, or 3")
        continue
