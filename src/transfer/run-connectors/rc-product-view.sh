#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "product-view-connector" \
  --inputs "persistent://public/default/product-view" \
  --tenant "public" \
  --sink-config-file /configs/c-product-view.yaml \
  --parallelism 1