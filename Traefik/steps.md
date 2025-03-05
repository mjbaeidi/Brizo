# Installing Traefik using Helm

## Prerequisites
- Kubernetes cluster (microk8s) up and running
- Helm installed
- kubectl configured

## Installation Steps

1. Add the Traefik Helm repository:
```bash
helm repo add traefik https://traefik.github.io/charts
```

2. Update Helm repositories:
```bash
helm repo update
```

3. Create namespace for Traefik:
```bash
kubectl create namespace traefik-system
```

4. Install Traefik using Helm with custom values:
```bash
helm install traefik traefik/traefik \
  --namespace traefik-system \
  -f myval.yaml
```

5. Verify the installation:
```bash
kubectl get pods -n traefik-system
```

6. Check Traefik dashboard access:
```bash
kubectl get svc -n traefik-system
```

The Traefik dashboard should be accessible at `http://<node-ip>:8080/dashboard/`

## Uninstall (if needed)
```bash
helm uninstall traefik -n traefik-system
```
