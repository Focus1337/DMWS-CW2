create table product_views
(
    timestamp  datetime,
    user_id    int,
    product_id int
) engine = MergeTree() order by timestamp;

create table sortings
(
    timestamp  datetime,
    user_id    int,
    price_min  double,
    price_max  double,
    rating_min double,
    rating_max double
) engine = MergeTree() order by timestamp;

create table cart_adds
(
    timestamp  datetime,
    user_id    int,
    product_id int,
    quantity   int
) engine = MergeTree() order by timestamp;

create table cart_removes
(
    timestamp  datetime,
    user_id    int,
    product_id int,
    quantity   int
) engine = MergeTree() order by timestamp;

create table review_views
(
    timestamp     datetime,
    user_id       int,
    review_id     int,
    review_rating int
) engine = MergeTree() order by timestamp;

create table coupon_uses
(
    timestamp datetime,
    user_id   int,
    coupon_id int,
    order_id  int
) engine = MergeTree() order by timestamp;

create table category_views
(
    timestamp          datetime,
    user_id            int,
    category_id        int,
    parent_category_id int
) engine = MergeTree() order by timestamp;