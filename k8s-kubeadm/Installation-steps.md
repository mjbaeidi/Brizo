# Kubernetes Installation Guide

## Prerequisites
- **Operating System:** Ubuntu 20.04 or later
- **User Permissions:** Root or a user with `sudo` privileges
- **Firewall:** Disabled or properly configured to allow Kubernetes traffic
- **Network Configuration:** Ensure nodes can communicate with each other

## Step 1: Update System Packages
```sh
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Required Packages
```sh
sudo apt install -y apt-transport-https ca-certificates curl
```

## Step 3: Disable Swap
```sh
sudo swapoff -a
sed -i '/swap/d' /etc/fstab
```

## Step 4: Load Kernel Modules
```sh
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
```

## Step 5: Configure Sysctl Settings
```sh
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
```

## Step 6: Install Containerd
```sh
sudo apt install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
sudo systemctl restart containerd
```

## Step 7: Install Kubernetes Components
```sh
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

## Step 8: Initialize Kubernetes Cluster (Control Plane Node)
```sh
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

## Step 9: Configure kubectl for the User
```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Step 10: Deploy a Network Plugin (Calico)
```sh
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

## Step 11: Join Worker Nodes to the Cluster
Run the `kubeadm join` command displayed after initializing the control plane on each worker node:
```sh
sudo kubeadm join <MASTER_IP>:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
```

## Step 12: Verify Cluster Status
```sh
kubectl get nodes
kubectl get pods -A
```

## Step 13: Enable kubectl Autocomplete (Optional)
```sh
echo 'source <(kubectl completion bash)' >> ~/.bashrc
source ~/.bashrc
```

