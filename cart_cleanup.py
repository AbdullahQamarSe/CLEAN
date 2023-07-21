# cart_cleanup.py
import os
import time
import django

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Enterprises_Connect.settings")
django.setup()

from Api.models import cart as Cart, product as Product

def cleanup_carts():
    while True:
        carts = Cart.objects.all()
        for cart in carts:
            cart.timeline -= 1  # Decrease the timeline by 1 second

            if cart.timeline <= 0:
                # Get the product associated with the cart using the 'pid'
                try:
                    product = Product.objects.get(pk=cart.pid)
                except Product.DoesNotExist:
                    # If the product doesn't exist, skip this cart
                    continue

                # Add the cart quantity back to the product quantity
                try:
                    product.quantity += int(cart.quantity)
                    product.save()
                except ValueError:
                    # Handle the case where cart quantity is not an integer
                    continue

                # Now, delete the cart
                cart.delete()
            else:
                cart.save()

        # Wait for 1 second before running the loop again
        time.sleep(1)

if __name__ == "__main__":
    cleanup_carts()
