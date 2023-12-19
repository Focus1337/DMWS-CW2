create table product_views (
    view_time datetime,
    user_id int,
    product_id int
) engine = MergeTree() order by view_time;

create table sortings (
    sort_time datetime,
    user_id int,
    price_min double,
    price_max double,
    rating_min double,
    rating_max double
) engine = MergeTree() order by sort_time;

create table cart_adds (
    add_time datetime,
    user_id int,
    product_id int,
    quantity int
) engine = MergeTree() order by add_time;

create table cart_removes (
    remove_time datetime,
    user_id int,
    product_id int,
    quantity int
) engine = MergeTree() order by remove_time;

create table review_views (
    view_time datetime,
    user_id int,
    review_id int,
    review_rating int
) engine = MergeTree() order by view_time;

create table coupon_uses (
    use_time datetime,
    user_id int,
    coupon_id int,
    order_id int
) engine = MergeTree() order by use_time;

create table category_views (
    view_time datetime,
    user_id int,
    category_id int,
    parent_category_id int
) engine = MergeTree() order by view_time;