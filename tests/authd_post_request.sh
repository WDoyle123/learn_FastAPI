curl -X 'POST' \
  'http://localhost:8000/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3MzYwOTQ4NDN9.qjS91ZLlflk15mnFche7i1jKOrJ2f6a8WoKcKEnAD_c' \
  -d '{
  "title": "string",
  "content": "string",
  "published": true
}' | jq
