#! /usr/bin/python3
"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.consumer_id = kwargs.get('name')

    def run(self):
        # For each cart
        for cart in self.carts:
            # Associate it a cart_id
            cart_id = self.marketplace.new_cart()
            # For each action in this cart
            for action in cart:
                if action.get('type') == 'add':
                    k = 0
                    # Try to add it in cart. If it fails, try again after retry_wait_time
                    while k < action.get('quantity'):
                        if not self.marketplace.add_to_cart(cart_id, action.get('product')):
                            sleep(self.retry_wait_time)
                            k = k - 1
                        k = k + 1
                elif action.get('type') == 'remove':
                    k = 0
                    # Remove product from 'action' from this cart
                    while k < action.get('quantity'):
                        # If it is not in this cart, wait
                        if not self.marketplace.remove_from_cart(cart_id, action.get('product')):
                            sleep(self.retry_wait_time)
                            k = k - 1
                        k = k + 1

            # For each cart, print what this consumer bought
            shopping_list = self.marketplace.place_order(cart_id)
            for item in shopping_list:
                print(str(self.consumer_id) + " bought " + str(item), flush=True)
