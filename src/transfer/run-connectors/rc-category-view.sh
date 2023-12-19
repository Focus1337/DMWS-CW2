#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "category-view-connector" \
  --inputs "persistent://public/default/category-view" \
  --tenant "public" \
  --sink-config-file /configs/c-category-view.yaml \
  --parallelism 1