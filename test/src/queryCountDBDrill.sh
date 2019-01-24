curl -X POST -H "Content-Type: application/json" \
    -d '{"queryType":"SQL", "query": \
    "select * from dfs.`/Users/joe-user/apache-drill-1.4.0/sample-data/donuts.json` \
    http://localhost:8047/query.json
