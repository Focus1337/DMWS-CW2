#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "review-view-connector" \
  --inputs "persistent://public/default/review-view" \
  --tenant "public" \
  --sink-config-file /configs/c-review-view.yaml \
  --parallelism 1