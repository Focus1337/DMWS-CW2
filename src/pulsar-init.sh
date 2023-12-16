#!/usr/bin/env sh

HOST="${PULSAR_HOST:-http://broker:8080}"

echo "Использую хост $HOST"

echo "Проверяю соединение к хосту $HOST"

WaitPulsarStartup()
{
    curl "$HOST" >/dev/null 2>/dev/null
    RESULT=$?
    until [ $RESULT -eq 0 ];
    do
        echo "Сервис еще недоступен"
        sleep 10
        echo "Делаю повторный запрос"
        curl "$HOST" >/dev/null 2>/dev/null
        RESULT=$?
    done
}

WaitPulsarStartup

# Создаем топики для работы
for topic in product-view sorting cart-add cart-remove review-view coupon-use category-view
do
  echo "Создаю топик $topic"
  /pulsar/bin/pulsar-admin --admin-url "$HOST" topics create "public/default/$topic"
done

echo "Топики созданы"

# Создаем коннекторы для каждого топика
for topic in product-view sorting cart-add cart-remove review-view coupon-use category-view
do
  TABLE_NAME=${topic%%-*}s
  TOPIC=$topic
  echo "configs:
    roots: "localhost:9042"
    keyspace: "pulsar_test_keyspace"
    columnFamily: "pulsar_test_table"
    keyname: "key"
    columnName: "col"" > /tmp/connector.yaml
  echo $TABLE_NAME
  echo "Создаю коннектор для $TOPIC"
  /pulsar/bin/pulsar-admin --admin-url "$HOST" sinks create \
    --tenant public \
    --namespace default \
    --name cassandra-$TOPIC \
    --sink-type cassandra \
    --sink-config-file /tmp/connector.yaml \
    --inputs $TOPIC
done

# Удаляем созданный конфиг файл
rm /tmp/connector.yaml