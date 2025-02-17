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

6. **Create a CephFS filesystem**
> **Note:** Pools and MDS (Metadata Servers) are created automatically.

