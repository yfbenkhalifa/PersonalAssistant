#!/bin/bash
# Stop Personal Assistant services

echo "🛑 Stopping Personal Assistant services..."
docker compose down

echo ""
echo "✅ Services stopped!"
echo ""
echo "To remove volumes and clean up completely, run:"
echo "  docker compose down -v"
echo ""
