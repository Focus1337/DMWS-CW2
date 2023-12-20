from clickhouse_driver import Client
from minio import Minio
from io import BytesIO

# Подключение к ClickHouse
clickhouse_client = Client('localhost', port=9000, secure=False)

# Подключение к MinIO
minio_client = Minio('localhost:9002',
                     access_key='minioadmin',
                     secret_key='minioadmin',
                     secure=False)

def insert_data_to_s3(table_name, bucket_name):
    # Выборка данных из ClickHouse
    query = f'SELECT * FROM {table_name}'
    data = clickhouse_client.execute(query)

    # Преобразование данных в формат, подходящий для записи в S3
    # В данном примере предполагается, что данные представлены в виде строк CSV
    formatted_data = '\n'.join([','.join(map(str, row)) for row in data])

    # Загрузка данных в S3
    object_key = f'{table_name}.csv'

    minio_client.put_object(
        bucket_name,
        object_key,
        data=BytesIO(formatted_data.encode('utf-8')),
        length=len(formatted_data),
        content_type='application/csv'  # Укажите соответствующий MIME-тип данных
    )

    print(f"Данные из таблицы {table_name} успешно загружены в бакет {bucket_name}")

# Пример использования:
table_name_to_export = 'product_views'
s3_bucket_name = 'dwms'
insert_data_to_s3(table_name_to_export, s3_bucket_name)
