curl -s -X POST http://localhost:8000/users \
    -H "Content-Type: application/json" \
    -d '{
        "email": "will.gmail.com",
        "password": "password123"
    }' | jq

