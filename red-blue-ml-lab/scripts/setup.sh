#!/bin/bash
# Red-Blue-ML Lab Setup Script

set -e

echo "=========================================="
echo "Red-Blue-ML Lab Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check Go (optional)
if command -v go &> /dev/null; then
    echo -e "${GREEN}✓ Go found${NC}"
else
    echo -e "${YELLOW}⚠ Go not found (optional for Go scenarios)${NC}"
fi

# Check Rust (optional)
if command -v cargo &> /dev/null; then
    echo -e "${GREEN}✓ Rust found${NC}"
else
    echo -e "${YELLOW}⚠ Rust not found (optional for Rust scenarios)${NC}"
fi

# Create directory structure
echo -e "\n${YELLOW}Creating directory structure...${NC}"
mkdir -p data/{raw,processed,features,logs}
mkdir -p models/saved
mkdir -p elk/{elasticsearch,logstash/pipelines,kibana/dashboards}
mkdir -p collectors/{filebeat,winlogbeat,packetbeat,custom}
mkdir -p scenarios/{01_initial_access,02_lateral_movement,03_exfiltration,04_persistence,05_evasion}
mkdir -p notebooks
mkdir -p cicd/{tests,scripts}
mkdir -p api
mkdir -p bin
mkdir -p logs
echo -e "${GREEN}✓ Directory structure created${NC}"

# Create Python virtual environment
echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Build Go scenarios (if Go is available)
if command -v go &> /dev/null; then
    echo -e "\n${YELLOW}Building Go scenarios...${NC}"
    if [ -d "scenarios/go" ]; then
        cd scenarios/go
        go mod init red-blue-ml-lab 2>/dev/null || true
        go mod tidy
        go build -o ../../bin/lateral_movement
        cd ../..
        echo -e "${GREEN}✓ Go scenarios built${NC}"
    fi
fi

# Build Rust scenarios (if Rust is available)
if command -v cargo &> /dev/null; then
    echo -e "\n${YELLOW}Building Rust scenarios...${NC}"
    if [ -d "scenarios/rust" ]; then
        cd scenarios/rust
        cargo build --release
        cp target/release/dns_tunnel ../../bin/
        cd ../..
        echo -e "${GREEN}✓ Rust scenarios built${NC}"
    fi
fi

# Create configuration files
echo -e "\n${YELLOW}Creating configuration files...${NC}"

# Elasticsearch config
cat > elk/elasticsearch/elasticsearch.yml << EOF
cluster.name: red-blue-ml-lab
node.name: node-1
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node

# ML settings
xpack.ml.enabled: true
xpack.security.enabled: false

# Index settings
index.number_of_shards: 1
index.number_of_replicas: 0
EOF

# Logstash config
cat > elk/logstash/logstash.yml << EOF
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch:9200"]
EOF

# Kibana config
cat > elk/kibana/kibana.yml << EOF
server.host: "0.0.0.0"
server.port: 5601
elasticsearch.hosts: ["http://elasticsearch:9200"]
EOF

# Filebeat config
cat > collectors/filebeat/filebeat.yml << EOF
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /logs/*.log
    fields:
      source: red-team
      lab: red-blue-ml

output.logstash:
  hosts: ["logstash:5000"]
EOF

echo -e "${GREEN}✓ Configuration files created${NC}"

# Pull Docker images
echo -e "\n${YELLOW}Pulling Docker images...${NC}"
docker-compose pull
echo -e "${GREEN}✓ Docker images pulled${NC}"

# Start ELK stack
echo -e "\n${YELLOW}Starting ELK stack...${NC}"
docker-compose up -d elasticsearch logstash kibana
echo -e "${GREEN}✓ ELK stack started${NC}"

# Wait for Elasticsearch to be ready
echo -e "\n${YELLOW}Waiting for Elasticsearch to be ready...${NC}"
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"'; do
    echo "Waiting for Elasticsearch..."
    sleep 5
done
echo -e "${GREEN}✓ Elasticsearch is ready${NC}"

# Create Elasticsearch indices
echo -e "\n${YELLOW}Creating Elasticsearch indices...${NC}"
curl -X PUT "localhost:9200/red-team-logs" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "scenario_id": { "type": "keyword" },
      "red_team_activity": { "type": "boolean" },
      "message": { "type": "text" },
      "source_ip": { "type": "ip" },
      "destination_ip": { "type": "ip" },
      "process_name": { "type": "keyword" },
      "command_line": { "type": "text" }
    }
  }
}
'
echo -e "\n${GREEN}✓ Elasticsearch indices created${NC}"

# Create .env file
echo -e "\n${YELLOW}Creating .env file...${NC}"
cat > .env << EOF
# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Logstash
LOGSTASH_HOST=localhost
LOGSTASH_PORT=5000

# Kibana
KIBANA_HOST=localhost
KIBANA_PORT=5601

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=redblueml
POSTGRES_USER=redblue
POSTGRES_PASSWORD=redblue123

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000
EOF
echo -e "${GREEN}✓ .env file created${NC}"

# Create Makefile
echo -e "\n${YELLOW}Creating Makefile...${NC}"
cat > Makefile << 'EOF'
.PHONY: help start stop restart logs clean test

help:
	@echo "Red-Blue-ML Lab Commands:"
	@echo "  make start     - Start all services"
	@echo "  make stop      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Clean up data and logs"
	@echo "  make test      - Run tests"
	@echo "  make notebook  - Start Jupyter notebook"

start:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf data/raw/* data/processed/* data/features/*
	rm -rf logs/*

test:
	pytest tests/

notebook:
	docker-compose up -d jupyter
	@echo "Jupyter available at http://localhost:8888"
EOF
echo -e "${GREEN}✓ Makefile created${NC}"

# Print success message
echo -e "\n${GREEN}=========================================="
echo "Setup completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Start all services: make start"
echo "2. Access Kibana: http://localhost:5601"
echo "3. Access Jupyter: http://localhost:8888"
echo "4. Access Grafana: http://localhost:3000"
echo "5. Run a scenario: python scenarios/01_initial_access/exploit.py"
echo ""
echo "For more information, see README.md"
