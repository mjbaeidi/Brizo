# Guide to Installing Cephfs

1. **Install cephadm using curl**

   ```sh
   curl --silent --remote-name https://raw.githubusercontent.com/ceph/ceph/master/src/cephadm/cephadm
   chmod +x cephadm
   ./cephadm install
   ```
2. **Bootstrap new cluster**

   ```sh
   sudo cephadm bootstrap --mon-ip <IP_ADDRESS>
   ```
3. **Add Ceph public key into authorized keys of other servers**

   ```sh
   sudo ceph cephadm get-pub-key > ceph.pub
   ssh-copy-id -f -i ceph.pub user@<OTHER_SERVER_IP>
   ```
4. **Install cephadm on each server**

   ```sh
   ssh user@<OTHER_SERVER_IP> 'curl --silent --remote-name https://raw.githubusercontent.com/ceph/ceph/master/src/cephadm/cephadm && chmod +x cephadm && sudo ./cephadm install'
   ```
5. **Go to dashboard and expand cluster by adding other servers**

   - Access the Ceph dashboard by navigating to `https://<MON_IP>:8443` in your web browser.
   - Login with the credentials provided during the bootstrap process.
   - Use the dashboard to add other servers to the cluster.
6. **Create a CephFS filesystem in dashboard**

> **Note:** Pools and MDS (Metadata Servers) are created automatically.

7. **Add Ceph-CSI repository in Helm and pull the chart**

   ```sh
   helm repo add ceph-csi https://ceph.github.io/csi-charts
   helm repo update
   helm pull ceph-csi/ceph-csi-cephfs --untar
   ```
8. **Update the values.yaml file**

   - Modify the `values.yaml` file to include the necessary configurations for your CephFS setup.
   - Example changes:

   ```yaml
   csiConfig: 
     - clusterID: 4dddb8b2-ec3f-11ef-82f3-005056bccd49
       monitors:
         - 10.192.127.239:6789
         - 10.192.127.237:6789
         - 10.192.127.229:6789
       cephFS:
         subvolumeGroup: "csi"
   storageClass:
     create: enable
     name: k8s-cephfs
     clusterID: 4dddb8b2-ec3f-11ef-82f3-005056bccd49
     fsName: mycephfs
     volumeNamePrefix: "poc-k8s-"
     provisionerSecret: csi-cephfs-secret
     controllerExpandSecret: csi-cephfs-secret
     nodeStageSecret: csi-cephfs-secret
     reclaimPolicy: Delete
     allowVolumeExpansion: true

   secret:
     create: true
     name: csi-cephfs-secret
     adminID: admin
     adminKey: AQCYoLFnJtJoAxAAlSLYQmMAHMkq1Gr3Hc3uWg==
   ```
