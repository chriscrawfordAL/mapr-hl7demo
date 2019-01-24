curl -X POST \
'https://mapr02.wired.carnoustie:8243/api/v2/table/%2Fdemos%2Fhl7demo%2Fd3%2FbarChartCount/document/MED_BAY_1' \
  -H 'Content-Type: application/json' \
  -u mapr:maprmapr18 \
  -k \
  -d '{"$increment":{"openBeds":1}}'
