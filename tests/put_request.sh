curl -s -X PUT http://localhost:8000/posts/2 \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Put Request",
        "content": "Put request content"
    }' | jq

