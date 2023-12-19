#!/usr/bin/env sh

# Создаем синк для ClickHouse
pulsar/bin/pulsar-admin sinks create \
  --sink-type 'jdbc-clickhouse' \
  --name "coupon-use-connector" \
  --inputs "persistent://public/default/coupon-use" \
  --tenant "public" \
  --sink-config-file /configs/c-coupon-use.yaml \
  --parallelism 1