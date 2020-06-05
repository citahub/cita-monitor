#!/usr/bin/env bash

language=$LANGUAGE
if [ "${language}" == "cn" ]; then
  while read -r line; do
    if [ "$line" != '' ]; then
      en=$(echo "$line" | awk -F: '{print $1}')
      cn=$(echo "$line" | awk -F: '{print $2}')
      en=$(eval echo "$en")
      cn=$(eval echo "$cn")
      sed -i s"#$en#$cn#g" /var/lib/grafana/dashboards/*.json
    fi
  done <language.ini
fi
