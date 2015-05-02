"""demo shopping cart application"""

class ShoppingCart(object):
	"""shopping cart that holds items with prices"""

	def __init__(self):
		""" create an emptty shopping cart"""
		self.items = []

	def add_item(self, item_name, item_price):
		"""add item and price to cart"""
		self.items.append((item_name, item_price

	def get_total(self):
		"""return the total cost of the items in the cart"""
		return 0


if __name__ == '__main__':
	cart = ShoppingCart()
	cart.add_item("carrots", 402)
	cart.add_item("cheap carrots", 0.99)