"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import unittest
from threading import Lock
from random import randint, seed
from tema.product import Coffee, Tea

seed()

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    # List of elements of type [producer_id, product, product_lock, product_availability]
    products = []
    # Dictionary with key-value pairs of type {'producer_id':[products_published]}
    producer_ids = {}
    # Lock for appending/removing items from products ' list
    products_lock = Lock()
    # Dictionary with key-value pairs of type {'cart_id': [cart_contents]}
    carts_id = {}
    # Lock for appending/removing items from carts_id ' dictionary
    carts_lock = Lock()

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

    # checked by unittest
    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Add the registered producer to the producer_ids dictionary
        producer_id = randint(1, 1000)
        while self.producer_ids.get(producer_id) is not None:
            producer_id = randint(1, 1000)
        self.producer_ids[producer_id] = 0
        return producer_id

    # checked twice by unittest
    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # If queue for this producer_id is full, wait until is emptied
        if self.producer_ids.get(producer_id) == self.queue_size_per_producer:
            return False
        # Create a lock for this product and add it to the 'products' list
        prod_lock = Lock()
        self.products_lock.acquire()
        self.products.append([producer_id, product, prod_lock, True])
        self.products_lock.release()

        return True

    # checked by unittest
    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # Create a random int as cart_id
        cart_id = randint(1, 1000)
        while self.carts_id.get(cart_id) is not None:
            cart_id = randint(1, 1000)
        self.carts_id[cart_id] = []
        return cart_id

    # Checked twice by unittest
    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # For each product in stock
        for prod in self.products:
            # If this prod is the product we are looking for
            if prod[1] == product:
                # If this product is available
                if prod[3]:
                    prod[2].acquire()
                    # Make it unavailable
                    prod[3] = False
                    self.carts_lock.acquire()
                    # Add it to this cart
                    self.carts_id[cart_id].append(prod[1])
                    self.carts_lock.release()
                    prod[2].release()
                    return True
        return False

    # checked twice by unittest
    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # For each product in stock
        for prod in self.products:
            # If this product is the one we are looking for and it's in this cart
            if prod[1] == product and product in self.carts_id.get(cart_id):
                prod[2].acquire()
                # Make it available
                prod[3] = True
                self.carts_lock.acquire()
                # Remove it from cart
                self.carts_id.get(cart_id).remove(prod[1])
                self.carts_lock.release()
                prod[2].release()
                return True
        return False

    # check twice by unittest
    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.products_lock.acquire()
        # For each product in stock
        for prod in self.products:
            # If this prod is in this cart and is unavailable in stock, remove it
            if prod[1] in self.carts_id.get(cart_id) and not prod[3]:
                self.products.remove(prod)
                # Make room for a producer to continue producing
                self.producer_ids[prod[0]] = self.producer_ids.get(prod[0]) - 1
        self.products_lock.release()
        return self.carts_id[cart_id]

class TestMarketplace(unittest.TestCase):
    """
    Testing methods from Marketplace class
    """
    def setUp(self):
        """
        Sets up the environment for tests
        """
        self.marketplace = Marketplace(1)
        self.product1 = Coffee(name='Indonezia', price=1, acidity=5.05, roast_level='MEDIUM')
        self.product2 = Tea(name='Linden', price=9, type='Herbal')
        self.producer_id = 'prod1'
        self.marketplace.publish(self.producer_id, self.product1)
        self.marketplace.publish(self.producer_id, self.product2)
        self.marketplace.register_producer()
        self.cart_id = self.marketplace.new_cart()

    def test_register_producer(self):
        """ check if the producer is successfully registered"""
        number = self.marketplace.register_producer()
        val = 1 <= number <= 1000
        self.assertTrue(val)

    def test_new_cart(self):
        """ check if the cart_id is generated successfully"""
        number = self.marketplace.new_cart()
        val = 1 <= number <= 1000
        self.assertTrue(val)

    def test_publish_succesful(self):
        """
        Check if a product is added to the stock.
        Return true.
        """
        self.assertTrue(self.marketplace.publish(self.producer_id, self.product1))

    def test_publish_fail(self):
        """
        This shall fail because there is no more room in stock.
        """
        self.marketplace.queue_size_per_producer = 0
        self.assertFalse(self.marketplace.publish(self.producer_id, self.product1))

    def test_add_to_cart_fail(self):
        """
        This should fail because the product is unavailable.
        """
        self.marketplace.products[0][3] = False
        val = self.marketplace.add_to_cart(self.cart_id, self.marketplace.products[0][1])
        self.assertFalse(val)

    def test_add_to_cart_succesful(self):
        """
        Checks if the product from stock is added successfully in
        this cart.
        """
        val = self.marketplace.add_to_cart(self.cart_id, self.marketplace.products[1][1])
        self.assertTrue(val)

    def test_remove_from_cart_succesful(self):
        """
        Check if the item from the cart is removed and added back to stock
        """
        self.marketplace.add_to_cart(self.cart_id, self.product1)
        self.assertTrue(self.marketplace.remove_from_cart(self.cart_id, self.product1))

    def test_remove_from_cart_fail(self):
        """
        This should fail because there is no item in cart
        """
        self.assertFalse(self.marketplace.remove_from_cart(self.cart_id, self.product1))

    def test_place_order_non_empty(self):
        """
        Check to see if all items in cart are ordered
        """
        self.marketplace.add_to_cart(self.cart_id, self.product1)
        shopping_list = self.marketplace.place_order(self.cart_id)
        self.assertEqual(shopping_list[0], self.product1)

    def test_place_order_empty(self):
        """
        Check to see the behaviour if the cart is empty
        """
        shopping_list = self.marketplace.place_order(self.cart_id)
        self.assertEqual(shopping_list, [])

if __name__ == '__main__':
    unittest.main()
