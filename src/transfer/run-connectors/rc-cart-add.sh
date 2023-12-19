#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "cart-add-connector" \
  --inputs "persistent://public/default/cart-add" \
  --tenant "public" \
  --sink-config-file /configs/c-cart-add.yaml \
  --parallelism 1