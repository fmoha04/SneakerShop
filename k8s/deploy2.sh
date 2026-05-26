#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Deploying from: $SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Creating SSL Certificate Secret...${NC}"
# Create SSL certificate secret from local certs
if [ -f "../certs/cert.pem" ] && [ -f "../certs/key.pem" ]; then
    kubectl delete secret grupo7a-certs -n grupo7a 2>/dev/null || true
    kubectl create secret generic grupo7a-certs \
        --from-file=cert.pem=../certs/cert.pem \
        --from-file=key.pem=../certs/key.pem \
        -n grupo7a || echo "Secret already exists"
else
    echo "ERROR: Certificates not found at ../certs/cert.pem or ../certs/key.pem"
    exit 1
fi

echo -e "${BLUE}2. Applying configuration secrets...${NC}"
kubectl apply -f "$SCRIPT_DIR/secrets.yml"

echo -e "${BLUE}3. Applying persistent volumes...${NC}"
kubectl apply -f "$SCRIPT_DIR/pv_volume.yml"
kubectl apply -f "$SCRIPT_DIR/pvc_volume.yml"

echo -e "${BLUE}4. Deploying MariaDB...${NC}"
kubectl apply -f "$SCRIPT_DIR/mariadb_configmap.yml"
kubectl apply -f "$SCRIPT_DIR/mariadb_deployment.yml"
kubectl apply -f "$SCRIPT_DIR/mariadb_service.yml"
echo "Waiting for MariaDB to be ready..."
kubectl wait --for=condition=ready pod -l app=mariadb -n grupo7a --timeout=300s

echo -e "${BLUE}5. Deploying Python API...${NC}"
kubectl apply -f "$SCRIPT_DIR/python_deployment.yml"
kubectl apply -f "$SCRIPT_DIR/python_service.yml"
echo "Waiting for Python API to be ready..."
kubectl wait --for=condition=ready pod -l app=python -n grupo7a --timeout=300s

echo -e "${BLUE}6. Deploying Apache Frontend...${NC}"
kubectl apply -f "$SCRIPT_DIR/apache_deployment.yml"
kubectl apply -f "$SCRIPT_DIR/apache_service.yml"
echo "Waiting for Apache to be ready..."
kubectl wait --for=condition=ready pod -l app=apache -n grupo7a --timeout=300s

# echo -e "${BLUE}7. Deploying PhpMyAdmin (commented out)...${NC}"
# kubectl apply -f "$SCRIPT_DIR/phpmyadmin_deployment.yml"
# kubectl apply -f "$SCRIPT_DIR/phpmyadmin_service.yml"

echo -e "${GREEN}✓ Deployment complete!${NC}"
echo -e "${GREEN}Services:${NC}"
kubectl get svc -n grupo7a
echo -e "${GREEN}\nPods:${NC}"
kubectl get pods -n grupo7a
echo -e "\n${BLUE}Monitor logs:${NC}"
echo "kubectl logs -f -l app=python -n grupo7a"
echo "kubectl logs -f -l app=apache -n grupo7a"
echo "kubectl logs -f -l app=mariadb -n grupo7a"
