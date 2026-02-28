#!/usr/bin/env bash
set -euo pipefail

curl -s -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"demo","message":"Give me a 3-step productivity plan","use_voice":false}' | jq
