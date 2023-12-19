#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "sorting-connector" \
  --inputs "persistent://public/default/sorting" \
  --tenant "public" \
  --sink-config-file /configs/c-sorting.yaml \
  --parallelism 1