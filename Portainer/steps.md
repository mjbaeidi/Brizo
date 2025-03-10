# Guide to Installing Portainer using Helm

## Prerequisites

- Kubernetes cluster up and running
- Helm installed on your system
- kubectl configured to interact with your cluster

## Installation Steps

1. **Add the Portainer Helm repository:**

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update
```

2. **Create namespace for Portainer:**

```bash
kubectl create namespace portainer
```

3. **Use the myval.yaml file provided in this directory for configuration values.**

4. **Install Portainer using Helm with values file:**

```bash
helm install portainer portainer/portainer \
    --namespace portainer \
    -f myval.yaml
```

5. **Verify the installation:**

```bash
kubectl get pods -n portainer
kubectl get svc -n portainer
```

6. **Access Portainer UI:**

```bash
kubectl get svc -n portainer portainer -w
```

Access the Portainer UI at:
- https://<NODE-IP>:<NODEPORT> (HTTPS)

Note: First login credentials must be set up within the first 24 hours after installation.
