from pulsar.schema import Record, String, Integer

class ProductViewEvent(Record):
    view_time = String()
    user_id = Integer()
    product_id = Integer()

class SortingEvent(Record):
    sort_time = String()
    user_id = Integer()
    price_min = Integer()
    price_max = Integer()
    rating_min = Integer()
    rating_max = Integer()

class CartAddEvent(Record):
    add_time = String()
    user_id = Integer()
    product_id = Integer()
    quantity = Integer()

class CartRemoveEvent(Record):
    remove_time = String()
    user_id = Integer()
    product_id = Integer()
    quantity = Integer()

class ReviewViewEvent(Record):
    view_time = String()
    user_id = Integer()
    review_id = Integer()
    review_rating = Integer()

class CouponUseEvent(Record):
    use_time = String()
    user_id = Integer()
    coupon_id = Integer()
    order_id = Integer()

class CategoryViewEvent(Record):
    view_time = String()
    user_id = Integer()
    category_id = Integer()
    parent_category_id = Integer()