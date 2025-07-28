# Installing Velero on Kubernetes

This guide provides step-by-step instructions for installing Velero on a Kubernetes cluster to back up its resources.

## Prerequisites

*   A running Kubernetes cluster.
*   `kubectl` configured to interact with your cluster.
*   Necessary CRDs for volume snapshotting. If you don't have them, you can install them by following the official Kubernetes guide for your CSI driver. For many common drivers, you can install the necessary CRDs with the following commands:
    ```bash
    kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
    kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
    kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
    ```
*   An S3 compatible bucket created in advance (This document use Minio as S3 compatible). In this guide, the bucket is named `velero`.
*   A credentials file for your S3 provider. In this guide, it is named `credentials-velero` and located in the same directory where you run the installation command.

## Installation Steps

1.  **Download and Install Velero CLI:**
    Download the latest Velero release from the [official GitHub repository](https://github.com/vmware-tanzu/velero/releases). Extract the tarball and move the `velero` executable to a directory in your system's `PATH`, for example `/usr/local/bin`.
    ```bash
    # Example for Linux
    wget https://github.com/vmware-tanzu/velero/releases/download/v1.16.1/velero-v1.16.1-linux-amd64.tar.gz
    tar -xvf velero-v1.16.1-linux-amd64.tar.gz
    sudo mv velero-v1.16.1-linux-amd64/velero /usr/local/bin/
    ```

2.  **Create Namespace (if it doesn't exist):**
    The installation command specifies the `velero` namespace. Create it if it doesn't exist:
    ```bash
    kubectl create namespace velero
    ```

3.  **Install Velero:**
    Deploy Velero using the `velero install` command. This command sets up Velero with the AWS provider, configures the S3 bucket location, and enables CSI snapshot support.
    ```bash
    velero install --use-node-agent --privileged-node-agent --provider aws \
        --namespace velero \
        --plugins velero/velero-plugin-for-aws:v1.2.1 \
        --bucket velero \
        --secret-file ./credentials-velero \
        --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=https://{your-s3-url} \
        --features=EnableCSI
    ```
    This command installs Velero into the `velero` namespace using the specified configurations.

4.  **Verify Installation:**
    Check the status of the Velero deployment to ensure all pods are running correctly.
    ```bash
    kubectl get pods -n velero
    ```
    You should see the `velero` and `node-agent` pods in a `Running` state.

## Creating a Backup

Once Velero is installed and running, you can create backups of your Kubernetes resources.

1.  **Create a VolumeSnapshotClass:**
    Before creating a backup, you need to create a `VolumeSnapshotClass` to instruct Velero on how to take snapshots. You can use the `volumeSnapshotclass.yml` file located in this directory.
    Apply the configuration to your cluster:
    ```bash
    kubectl apply -f volumeSnapshotclass.yml
    ```

2.  **Label Resources for Backup:**
    The example backup command uses a label selector (`isbackup=true`) to identify which resources to include. You need to label the resources you want to back up. For example, to label a PersistentVolume (PV) and a PersistentVolumeClaim (PVC):
    ```bash
    kubectl label pv <your-pv-name> isbackup=true
    kubectl label pvc <your-pvc-name> -n <your-namespace> isbackup=true
    ```

3.  **Run the Backup Command:**
    Use the `velero backup create` command to initiate a backup. The following command creates a backup named `new-backup`, includes PVs and PVCs that match the `isbackup=true` selector, and moves the data from the snapshots.
    ```bash
    velero backup create new-backup --snapshot-move-data --selector isbackup=true --include-resources pv,pvc
    ```

4.  **Check Backup Status:**
    You can check the status of your backup with the following command:
    ```bash
    velero backup describe new-backup
    ```
    Look for `Phase: Completed` to confirm the backup was successful.
