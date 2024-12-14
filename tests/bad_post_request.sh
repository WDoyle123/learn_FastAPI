curl -s -X POST http://localhost:8000/createposts \
    -H "Content-Type: application/json" \
    -d '{
        "content": "this is a film"
    }' | jq

