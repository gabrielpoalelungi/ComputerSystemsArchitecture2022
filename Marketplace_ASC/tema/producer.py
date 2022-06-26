"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()

    def run(self):

        while True:
            # For each product to be published (product = [product, quantity, wait_time])
            for prod in self.products:
                no_prod = 0
                # For each quantity 'no_prod'
                while no_prod < prod[1]:
                    new_prod = prod[0]
                    # Try to publish it. If it fails, wait and try again
                    if not self.marketplace.publish(self.producer_id, new_prod):
                        no_prod = no_prod - 1
                        sleep(self.republish_wait_time)
                    else:
                        nr_products = self.marketplace.producer_ids.get(self.producer_id)
                        self.marketplace.producer_ids[self.producer_id] = nr_products + 1
                        sleep(prod[2])
                    no_prod = no_prod + 1
