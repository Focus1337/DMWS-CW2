#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "cart-remove-connector" \
  --inputs "persistent://public/default/cart-remove" \
  --tenant "public" \
  --sink-config-file /configs/c-cart-remove.yaml \
  --parallelism 1