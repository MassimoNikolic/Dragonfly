# Dragonfly

Developed by: Massimo Nikolic

# Problem

The main goal of my project was to create an e-Commerce pub/sub program where users can find and buy items from providers.

# Framework
 
For this assignment, I chose to use the ZeroMQ framework for making my distributed system. I decided to implement a Pub/Sub system for the distributed computing component where the publishers act as providers of the items and subscriber are customers that access the items through subscribing to the publisher's items.

# How to Run

Run the system by running the given files in separate terminal instances.

# manager.py

This module contains socket components that act as a proxy for the system. Run this in a terminal to enable the pub/sub interactions of the whole system. Perform a KeyboardInterrupt with Ctrl+C to shut down the proxy.

# pub_server.py

This module contains code for the publisher. It stores the items it provides as strings in a dictionary called "product_listing" where the key is the item and the value is the amount of that item in stock. Run the code in its own terminal to have it periodically broadcast messages of all items in its listing. The item name is the topic of the message, and the amount in stock is the data sent. Perform a KeyboardInterrupt with Ctrl+C to shut down the proxy.

# sub_client.py

This module contains code for the subscriber. Run the code in its own terminal to start the client. You will be given 3 options to select from: checking available items, purchasing items, and quitting out of the application. 

The check option prints out the first 3 messages received by active publishers at the time of starting the check. This will print out the item names to type in for purchasing and the amount available in stock. 

The purchase option will ask you to enter the name of the wanted item; you can also enter "quit" to return to the option select. Entering a valid name will make you subscribe to that item's topic, and your client will then listen out for any messages of that item provided by the publisher. If your item does not show up within a given time, or you enter an invalid name, the client will time out and return you to the main option select. Once you receive the message, you will be given an option of (Y)es or (n)o [(Y/n)] for if you want to purchase the item. Entering "y" will bring up a prompt asking for how much of the item you will be purchasing. Enter your desired amount, and that will complete the transaction and loop back to the option select.

The quit option is self-explanatory.

You can run multiple instances of this module in each of their own terminals to simulate multiple subscribers.

# TODO

- Implement upstream message communication so that subscribers' item purchases will decrement the amount available in the respective publisher product_listing.
- Implement capability for publishers to save any changes to their stock values (Which may require an overhaul of the product_listing to use either csv files, a database, or some other data structure).