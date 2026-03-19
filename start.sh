#!/bin/bash
# Personal Assistant - Quick Start Script

set -e

echo "🚀 Personal Assistant - Docker Setup"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your API credentials:"
        echo "   - AZURE_OPENAI_ENDPOINT"
        echo "   - AZURE_OPENAI_API_KEY"
        echo ""
        echo "   Run: nano .env"
        echo ""
        exit 1
    else
        echo "❌ .env.example not found!"
        exit 1
    fi
fi

# Parse arguments
BUILD=false
DETACHED=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --build|-b)
            BUILD=true
            shift
            ;;
        --detached|-d)
            DETACHED=true
            shift
            ;;
        --help|-h)
            echo "Usage: ./start.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -b, --build       Rebuild containers before starting"
            echo "  -d, --detached    Run in detached mode (background)"
            echo "  -h, --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./start.sh              # Start services"
            echo "  ./start.sh --build      # Rebuild and start"
            echo "  ./start.sh -b -d        # Rebuild, start in background"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run with --help for usage information"
            exit 1
            ;;
    esac
done

# Build command
CMD="docker compose up"

if [ "$BUILD" = true ]; then
    echo "🔨 Building containers..."
    CMD="$CMD --build"
fi

if [ "$DETACHED" = true ]; then
    CMD="$CMD -d"
else
    echo "💡 Tip: Press Ctrl+C to stop the services"
fi

echo ""
echo "Starting services..."
echo "Command: $CMD"
echo ""

# Run docker-compose
eval $CMD

if [ "$DETACHED" = true ]; then
    echo ""
    echo "✅ Services started in background!"
    echo ""
    echo "📡 Access points:"
    echo "   Frontend:  http://localhost:8080"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📊 View logs:  docker compose logs -f"
    echo "🛑 Stop:       docker compose down"
    echo ""
fi
