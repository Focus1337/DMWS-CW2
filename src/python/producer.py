import pulsar
from events import (
    CouponUseEvent,
    ProductViewEvent,
    SortingEvent,
    CartAddEvent,
    CartRemoveEvent,
    ReviewViewEvent,
    CategoryViewEvent
)
from pulsar.schema import AvroSchema
import random
import time
from datetime import datetime

client = pulsar.Client("pulsar://localhost:6650")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def random_user():
    return random.randint(1, 10000)    

def random_review_rating():
    return random.randint(1, 5)

def random_product():
    return random.randint(1, 100)

try:
    product_view_producer = client.create_producer(
        "product-view", schema=AvroSchema(ProductViewEvent)
    )
    sorting_producer = client.create_producer(
        "sorting", schema=AvroSchema(SortingEvent)
    )
    cart_add_producer = client.create_producer(
        "cart-add", schema=AvroSchema(CartAddEvent)
    )
    cart_remove_producer = client.create_producer(
        "cart-remove", schema=AvroSchema(CartRemoveEvent)
    )
    review_view_producer = client.create_producer(
        "review-view", schema=AvroSchema(ReviewViewEvent)
    )
    coupon_use_producer = client.create_producer(
        "coupon-use", schema=AvroSchema(CouponUseEvent)
    )
    category_view_producer = client.create_producer(
        "category-view", schema=AvroSchema(CategoryViewEvent)
    )

    while True:
        random_number = random.randint(1, 7)
        if random_number == 1:
            producer = product_view_producer
            event = ProductViewEvent(
                timestamp=now(),
                user_id=random_user(),
                product_id=random_product(),
            )
        if random_number == 2:
            producer = sorting_producer
            event = SortingEvent(
                timestamp=now(),
                user_id=random_user(),
                price_min=random.randint(0, 1),
                price_max=random.randint(0, 1),
                rating_min=random.randint(0, 1),
                rating_max=random.randint(0, 1)
            )
        if random_number == 3:
            producer = cart_add_producer
            event = CartAddEvent(
                timestamp=now(),
                user_id=random_user(),
                product_id = random_product(),
                quantity = random.randint(1, 5)
            )
        if random_number == 4:
            producer = cart_remove_producer
            event = CartRemoveEvent(
                timestamp=now(),
                user_id=random_user(),
                product_id = random_product(),
                quantity = random.randint(1, 5)
            )
        if random_number == 5:
            producer = review_view_producer
            event = ReviewViewEvent(
                timestamp=now(),
                user_id=random_user(),
                review_id=random.randint(1, 50),
                review_rating=random_review_rating()
            )
        if random_number == 6:
            producer = coupon_use_producer
            event = CouponUseEvent(
                timestamp=now(),
                user_id=random_user(),
                coupon_id=random.randint(1, 10),
                order_id=random_user()
            )
        if random_number == 7:
            producer = category_view_producer
            event = CategoryViewEvent(
                timestamp=now(),
                user_id=random_user(),
                category_id=random.randint(1, 10),
                parent_category_id=random.randint(1, 10)
            )

        print("producing " + str(random_number))
        producer.send(event)
        time.sleep(1)
finally:
    client.close()