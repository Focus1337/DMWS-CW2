import logging
import multiprocessing
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread
from typing import Type

import pulsar

from events import create_client, get_all_topics, BaseRecord, process_message, get_all_events

from hdfs import InsecureClient

logging.basicConfig(level=logging.DEBUG)

root_logger = logging.getLogger()

hdfs_url = 'http://localhost:9870'
root_logger.info('Устанавливаю адрес HDFS: %s', hdfs_url)

hdfs_client = InsecureClient(hdfs_url)
# Чтобы одновременно несколько потоков не могли выполнить запрос
hdfs_client_lock = Lock()

max_file_size_bytes = 1024 * 1024

def run_consumer(record_type: Type[BaseRecord], client: pulsar.Client):
    logger = logging.getLogger(f'Consumer({record_type.topic()})')
    logger.info('Подписываюсь на топик')
    consumer = client.subscribe(
        topic=record_type.topic(),
        subscription_name='hadoop-saver',
        schema=record_type.get_schema()
    )
    try:
        logger.info('Начинаю чтение сообщений')
        while True:
            message = consumer.receive()
            logger.debug('Получено сообщение')
            hdfs_client_lock.acquire(blocking=True)
            try:
                process_message(message, hdfs_client, logger, max_file_size_bytes=max_file_size_bytes)
            finally:
                hdfs_client_lock.release()
            consumer.acknowledge(message)
    finally:
        consumer.close()


def main():
    service_url = "pulsar://localhost:6650"
    root_logger.info('Создаю клиента для адреса %s', service_url)
    with create_client(service_url) as client:
        root_logger.debug('Создаю потоки консьюмеров')
        events = get_all_events()
        threads = [
            Thread(target=run_consumer, args=(event, client))
            for event in events
        ]
        root_logger.info('Запускаю потоки консьюмеров')
        for thread in threads:
            thread.start()

        root_logger.info('Потоки запущены. Ожидаю завершения')
        for thread in threads:
            thread.join()
        root_logger.info('Потоки завершили выполнение')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        root_logger.critical('Необработанное исключение', exc_info=e)
        exit(1)