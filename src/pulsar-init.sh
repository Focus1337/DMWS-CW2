# https://pulsar.apache.org/docs/3.1.x/client-libraries-python-use/

import pulsar
from events import (
    CouponUseEvent,
    SupportCallEvent,
    RefundEvent,
    ProductViewEvent,
    RecommendationViewEvent,
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


try:
    CouponUseEvent_producer = client.create_producer(
        "CouponUseEvent-topic", schema=AvroSchema(CouponUseEvent)
    )
    SupportCallEvent_producer = client.create_producer(
        "SupportCallEvent-topic", schema=AvroSchema(CouponUseEvent)
    )
    RefundEvent_producer = client.create_producer(
        "RefundEvent-topic", schema=AvroSchema(CouponUseEvent)
    )
    ProductViewEvent_producer = client.create_producer(
        "ProductViewEvent-topic", schema=AvroSchema(CouponUseEvent)
    )
    RecommendationViewEvent_producer = client.create_producer(
        "RecommendationViewEvent-topic", schema=AvroSchema(CouponUseEvent)
    )
    # ...
    id = 0
    while True:
        id += 1
        random_number = random.randint(1, 1)
        if random_number == 1:
            producer = CouponUseEvent_producer
            event = CouponUseEvent(
                coupon_id=random.randint(1, 10),
                user_id=random_user(),
                datetime=now(),
            )
        if random_number == 2:
            producer = SupportCallEvent_producer
            event = SupportCallEvent(
                user_id=random_user(),
                datetime=now(),
            )
        if random_number == 3:
            producer = RefundEvent_producer
            event = RefundEvent(
                seller_id=random.randint(1, 50),
                user_id=random_user(),
                datetime=now(),
            )
        if random_number == 4:
            producer = ProductViewEvent_producer
            event = ProductViewEvent(
                product_id=random.randint(1, 100),
                user_id=random_user(),
                datetime=now(),
            )
        if random_number == 5:
            producer = RecommendationViewEvent_producer
            event = RecommendationViewEvent(
                user_id=random_user(),
                datetime=now(),
            )

        print("producing " + event)
        producer.send(event)
        time.sleep(1)  # ждем секунду

finally:
    client.close()