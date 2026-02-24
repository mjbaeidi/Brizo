# Kubernetes Cluster Upgrade Guide

This document provides step-by-step instructions for upgrading a Kubernetes cluster. Follow the sections below based on your cluster setup.

---

## Pre-Upgrade Steps

### Backup ETCD
```bash
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save etcd-snapshot-pre-upgrade.db
```

Verify the snapshot:
```bash
etcdctl --write-out=table snapshot status etcd-snapshot-pre-upgrade.db
```

### Backup Calico Resources
```bash
for resource in ippool bgppeer hostendpoint globalnetworkpolicy networkpolicy felixconfiguration bgpconfiguration clusterinformation; do
  echo "Backing up $resource..."
  calicoctl get $resource -o yaml >> calico-resources-backup.yaml
  echo "---" >> calico-resources-backup.yaml
done
```

---

## Master Node 1 Upgrade

### Update Kubernetes Repository
```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

apt update
apt-cache madison kubeadm
```

### Upgrade Kubeadm
```bash
apt-mark unhold kubeadm && \
apt-get update && sudo apt-get install -y kubeadm='1.33.X-*' && \
apt-mark hold kubeadm
```

### Plan the Upgrade
```bash
kubeadm upgrade plan
```

### Apply the Upgrade
Gracefully shut down the API server:
```bash
killall -s SIGTERM kube-apiserver
sleep 20
```

Apply the upgrade:
```bash
kubeadm upgrade apply v1.33.8
```

### Update Calico
```bash
curl https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/calico.yaml -o upgrade.yaml
kubectl apply --server-side --force-conflicts -f upgrade.yaml
watch kubectl get pods -n kube-system
```

Update `calicoctl`:
```bash
curl -L https://github.com/projectcalico/calico/releases/download/v3.31.3/calicoctl-linux-amd64 -o calicoctl
chmod +x calicoctl
calicoctl version
```

### Upgrade Kubelet and Kubectl
```bash
kubectl drain k8s-master01 --ignore-daemonsets

apt-mark unhold kubelet kubectl && \
apt-get update && sudo apt-get install -y kubelet='1.33.8-*' kubectl='1.33.8-*' && \
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet

kubectl uncordon k8s-master01
```

---

## Other Master Nodes Upgrade

Repeat the following steps for each additional master node:

### Update Kubernetes Repository
```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg --yes

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

apt update
apt-cache madison kubeadm
```

### Upgrade Kubeadm
```bash
apt-mark unhold kubeadm && \
apt-get update && sudo apt-get install -y kubeadm='1.33.8-*' && \
apt-mark hold kubeadm
```

### Upgrade Node
Gracefully shut down the API server:
```bash
killall -s SIGTERM kube-apiserver
sleep 20
```

Upgrade the node:
```bash
kubeadm upgrade node
```

### Upgrade Kubelet and Kubectl
```bash
kubectl drain k8s-master03 --ignore-daemonsets

apt-mark unhold kubelet kubectl && \
apt-get update && sudo apt-get install -y kubelet='1.33.8-*' kubectl='1.33.8-*' && \
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet

kubectl uncordon k8s-master03
```

---

## Worker Nodes Upgrade

Repeat the following steps for each worker node:

### Update Kubernetes Repository
```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg --yes

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

### Upgrade Kubeadm
```bash
apt-mark unhold kubeadm && \
apt-get update && sudo apt-get install -y kubeadm='1.33.8-*' && \
apt-mark hold kubeadm
```

### Upgrade Node
```bash
kubeadm upgrade node
```

### Upgrade Kubelet and Kubectl
```bash
kubectl drain k8s-worker03 --ignore-daemonsets

apt-mark unhold kubelet kubectl && \
apt-get update && sudo apt-get install -y kubelet='1.33.8-*' kubectl='1.33.8-*' && \
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet

kubectl uncordon k8s-worker03
```