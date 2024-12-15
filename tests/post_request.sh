curl -s -X POST http://localhost:8000/posts \
    -H "Content-Type: application/json" \
    -d '{
        "title": "starwars",
        "content": "this is a film"
    }' | jq

