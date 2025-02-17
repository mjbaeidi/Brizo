# Guide to Installing MicroK8s

## Prerequisites

- Ensure unique hostnames for each node
- Check hostname on each machine:

```bash
hostname
```

## Installation

1. **Install MicroK8s using Snap:**

```bash
sudo snap install microk8s --classic --channel=1.32/stable
```

2. **On the primary node, generate the join command:**

```bash
microk8s add-node
```

This will output a command like:

```bash
microk8s join 192.168.1.100:25000/abcdefghijklmnop
```

3. **Join the cluster from secondary nodes:**

- Copy the join command from the primary node
- Run it on each secondary node you want to add to the cluster

```bash
microk8s join <primary-node-ip>:25000/<token> --worker
```

4. **Verify the cluster:**

```bash
microk8s kubectl get nodes
```

Note: Wait a few minutes after joining for the nodes to become ready.
