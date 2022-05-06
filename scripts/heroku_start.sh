#!/bin/bash

pip install .

cat > config/database.cfg << 'EOF'
[production]
url=${DATABASE_URL}
EOF

bots_query=$(echo "select * from bots;" | psql $DATABASE_URL)
error="ERROR"

if [[ "$bots_query" == *"$error"* ]]; then
  echo "Config Found, booting"
  grace start
else
  echo "Config not found, seeding new one"
  grace db create
  grace db seed
  grace start
fi
