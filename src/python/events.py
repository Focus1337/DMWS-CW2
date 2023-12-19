import contextlib
import csv
import io
import logging
import os
from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Type, ContextManager

import faker
import hdfs
import pulsar
from pulsar.schema import Record, String, Integer, Double


faker = faker.Faker(locale='ru')
event_classes: list[Type['BaseRecord']] = []
topic_to_event: dict[str, Type['BaseRecord']] = {}


def create_random_event() -> 'BaseRecord':
    cls = faker.random.choice(event_classes)
    return cls.create_random()


def get_all_events() -> list[Type['BaseRecord']]:
    return event_classes

def random_nullable_double():
    if faker.boolean(30):
        return faker.random.random()
    return None


MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1Мб


def process_message(message: pulsar.Message, hdfs_client: hdfs.Client, logger: logging.Logger, max_file_size_bytes=MAX_FILE_SIZE_BYTES):
    # 1. Сериализуем запись в CSV
    topic_name: str = message.topic_name()
    if topic_name.startswith('persistent://public/default/'):
        topic_name = topic_name.removeprefix('persistent://public/default/')
    cls = topic_to_event[topic_name]
    csv_row = cls.serialize_csv(message.value())

    # 2. Записываем запись в CSV файл
    csv_path = f'C:/Users/Focus/Desktop/dwms-cw/src/python/tmp/{cls.filename()}'
    try:
        with open(csv_path, 'a') as file:
            file.write(csv_row)
            size_exceed = max_file_size_bytes < os.path.getsize(csv_path)
    except Exception as e:
        logger.critical('Ошибка во время записи CSV в файл %s', csv_path, exc_info=e)
        raise e

    # Если размер не превышен - завершаемся
    if not size_exceed:
        return

    # 3. Записываем файл в HDFS
    logger.info('Размер файла превысил максимальный. Отправляю в HDFS')
    hdfs_path = cls.filename()
    try:
        with open(csv_path, 'rb') as file:
            try:
                hdfs_client.write(hdfs_path, data=file, replication=1, append=True)
            except hdfs.util.HdfsError:
                try:
                    hdfs_client.write(hdfs_path, data=file, replication=1, append=False)
                except hdfs.util.HdfsError as hdfs_error:
                    logger.warning(f'Ошибка при дозаписи в файл {hdfs_path}', exc_info=hdfs_error)
    except Exception as e:
        logger.critical('Ошибка во время отправки чанка в HDFS', exc_info=e)
        raise e

    # 4. Удаляем старый файл (ставим размер в 0)
    try:
        with open(csv_path, 'w') as file:
            file.truncate(0)
    except Exception as e:
        logger.critical('Ошибка во время удаления большого файла', exc_info=e)
        raise e


@contextlib.contextmanager
def create_client(service_url='pulsar://localhost:6650') -> ContextManager[pulsar.Client]:
    client = pulsar.Client(service_url, authentication=pulsar.AuthenticationBasic(username='admin', password='apachepulsar'))
    try:
        yield client
    finally:
        client.close()


def get_all_topics():
    return [
        e.topic() for e in event_classes
    ]


class BaseRecord(Record):
    def __init_subclass__(cls):
        event_classes.append(cls)
        topic_to_event[cls.topic()] = cls

    @classmethod
    def filename(cls):
        return f'{cls.topic()}.csv'

    @classmethod
    def get_schema(cls) -> pulsar.schema.Schema:
        return pulsar.schema.AvroSchema(cls)

    @classmethod
    @abstractmethod
    def topic(cls):
        raise NotImplementedError()

    @classmethod
    def create_random(cls) -> 'BaseRecord':
        base = cls.create_custom_random()
        base.timestamp = (datetime.now() + timedelta(seconds=faker.random.randint(-10, 10))).strftime('%Y-%m-%d %H:%M:%S')
        base.user_id = faker.random.randint(0, 100)
        return base

    @classmethod
    @abstractmethod
    def create_custom_random(cls) -> 'BaseRecord':
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_custom_fields(cls, obj) -> list:
        raise NotImplementedError

    @classmethod
    def serialize_csv(cls, obj) -> str:
        s = io.StringIO()
        writer = csv.writer(s, delimiter=';', quotechar='"')
        fields = [
            obj.timestamp,
            obj.user_id
        ]
        fields.extend(cls.get_custom_fields(obj))
        writer.writerow(fields)
        return s.getvalue()


class ProductViewEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    product_id = Integer(required=True)

    @classmethod
    def topic(cls):
        return 'product-view'

    @classmethod
    def get_custom_fields(cls, obj):
        return [obj.product_id]

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = ProductViewEvent()
        obj.product_id = faker.random.randint(0, 1000)
        return obj

class SortingEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    price_min = Integer()
    price_max = Integer()
    rating_min = Integer()
    rating_max = Integer()

    @classmethod
    def topic(cls):
        return 'sorting'

    @classmethod
    def get_custom_fields(cls, obj):
        return [
            obj.price_min, obj.price_max,
            obj.rating_min, obj.rating_max
        ]

    @classmethod
    def create_custom_random(cls):
        obj = SortingEvent()
        obj.price_min = random_nullable_double()
        obj.price_max = random_nullable_double()
        obj.rating_min = random_nullable_double()
        obj.rating_max = random_nullable_double()
        return obj

class CartAddEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    product_id = Integer(required=True)
    quantity = Integer(required=True)

    @classmethod
    def topic(cls):
        return 'cart-add'

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = CartAddEvent()
        obj.product_id = faker.random.randint(0, 1000)
        return obj

    @classmethod
    def get_custom_fields(cls, obj):
        return [
            obj.product_id
        ]

class CartRemoveEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    product_id = Integer(required=True)
    quantity = Integer(required=True)

    @classmethod
    def topic(cls):
        return 'cart-remove'

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = CartRemoveEvent()
        obj.product_id = faker.random.randint(0, 1000)
        return obj

    @classmethod
    def get_custom_fields(cls, obj):
        return [obj.product_id]

class ReviewViewEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    review_id = Integer(required=True)
    review_rating = Integer(required=True)

    @classmethod
    def topic(cls):
        return 'review-view'

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = ReviewViewEvent()
        obj.review_id = faker.random.randint(0, 1000)
        obj.review_rating = faker.random.randint(1, 5)
        return obj

    @classmethod
    def get_custom_fields(cls, obj):
        return [obj.review_id]

class CouponUseEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    coupon_id = Integer(required=True)
    order_id = Integer(required=True)

    @classmethod
    def topic(cls):
        return 'coupon-use'

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = CouponUseEvent()
        obj.coupon_id = faker.random.randint(0, 1000)
        obj.order_id = faker.random.randint(0, 1000)
        return obj

    @classmethod
    def get_custom_fields(cls, obj):
        return [
            obj.coupon_id,
            obj.order_id
        ]

class CategoryViewEvent(BaseRecord):
    timestamp = String(required=True)
    user_id = Integer(required=True)
    category_id = Integer(required=True)
    parent_category_id = Integer()

    @classmethod
    def topic(cls):
        return 'category-view'

    @classmethod
    def create_custom_random(cls) -> 'BaseRecord':
        obj = CategoryViewEvent()
        obj.category_id = faker.random.randint(0, 1000)
        if faker.random.random() < 0.3:
            obj.parent_category_id = faker.random.randint(0, 1000)
        return obj

    @classmethod
    def get_custom_fields(cls, obj):
        return [
            obj.category_id,
            obj.parent_category_id
        ]
