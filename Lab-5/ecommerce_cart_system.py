"""E-commerce shopping cart and checkout manager.

Handles adding and removing items, discounts, cart totals and
receipt export.
"""

import hashlib
import os
import secrets

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart. Returns False if it already exists."""
    if audit_log is None:
        audit_log = []
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart. Returns False if it was not there."""
    try:
        del cart_items[item_id]
    except KeyError:
        return False
    return True


def check_cart_status(item_id):
    """Return True if the item is in the cart with a positive quantity."""
    item = cart_items.get(item_id)
    if item is None:
        return False
    return item["qty"] > 0


def calculate_discounted_total(item_id, discount_rate):
    """Return the unit price of an item after a discount rate (0 to 1)."""
    base_price = cart_items[item_id]["price"]
    discount_rate = float(discount_rate)
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("discount_rate must be between 0 and 1")
    return base_price * (1 - discount_rate)


def calculate_cart_total(items):
    """Return the total value (price x quantity) of all items."""
    return sum(details["price"] * details["qty"] for details in items.values())


def generate_item_hash(item_id):
    """Return a SHA-256 hash of the item id."""
    return hashlib.sha256(item_id.encode()).hexdigest()


def generate_checkout_pin():
    """Return a secure random 4-digit checkout PIN."""
    return secrets.randbelow(9000) + 1000


def export_cart_receipt(filename="receipt.txt"):
    """Write the cart contents to a receipt file."""
    with open(filename, "w", encoding="utf-8") as receipt:
        receipt.write(str(cart_items))
    print("Receipt saved to:", filename)


def get_cart_summary(items):
    """Return the total number of units across all items."""
    return sum(details["qty"] for details in items.values()
               if details["qty"] > 0)


def main():
    """Run a sample checkout flow."""
    payment_gateway_key = os.environ.get("PAYMENT_GATEWAY_KEY", "")
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")
    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1", 0.10))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())
    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))
    print(f"Cart total: {calculate_cart_total(cart_items):.2f}")
    print("Gateway key configured:", bool(payment_gateway_key))


if __name__ == "__main__":
    main()
