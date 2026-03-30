FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp_road_trip_app/ ./mcp_road_trip_app/

# Expose port
EXPOSE 8080

# Run with ADK web server
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "mcp_road_trip_app"]
