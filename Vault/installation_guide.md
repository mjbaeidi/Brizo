# Installing Vault on Kubernetes using Helm

This guide provides step-by-step instructions for installing HashiCorp Vault on a Kubernetes cluster using the official Helm chart and a custom values file.

## Prerequisites

*   A running Kubernetes cluster.
*   `kubectl` configured to interact with your cluster.
*   Helm v3 installed.
*   The custom values file `my-values.yaml` located in the `Vault/` directory relative to where you run the Helm commands, or provide the correct path to it. The content of `Vault/my-values.yaml` is:
    ```yaml
    global:
      enable: true
      tlsDisable: false
      namespace: "vault-server" # Ensure this namespace exists or is created

    injector:
      enabled: true

    server:
      enable: true
      extraEnvironmentVars:
         VAULT_CACERT: /vault/userconfig/vault-tls/vault.ca
         VAULT_TLSCERT: /vault/userconfig/vault-tls/vault.crt
         VAULT_TLSKEY: /vault/userconfig/vault-tls/vault.key
      volumes:
        - name: userconfig-vault-tls
          secret:
            defaultMode: 420
            secretName: vault-tls # Ensure this secret exists and contains vault.ca, vault.crt, vault.key
      volumeMounts:
         - mountPath: /vault/userconfig/vault-tls
           name: userconfig-vault-tls
           readOnly: true

      dataStorage:
        storageClass: k8s-cephfs # Ensure this StorageClass exists

      standalone:
        enabled: true
        config: |-
          ui = true

          listener "tcp" {
            tls_disable = 0
            address = "[::]:8200"
            cluster_address = "[::]:8201"
            tls_cert_file = "/vault/userconfig/vault-tls/vault.crt"
            tls_key_file  = "/vault/userconfig/vault-tls/vault.key"
            tls_client_ca_file = "/vault/userconfig/vault-tls/vault.ca"
          }
          storage "file" {
            path = "/vault/data"
          }


    ui:
      enabled: true
      serviceType: "NodePort"
      serviceNodePort: 30820
    ```

## Installation Steps

1.  **Add HashiCorp Helm Repo & Update:**
    Add the HashiCorp Helm repository and update your local chart information:
    ```bash
    helm repo add hashicorp https://helm.releases.hashicorp.com
    helm repo update
    ```

2.  **Create Namespace (if it doesn't exist):**
    The `my-values.yaml` specifies the `vault-server` namespace. Create it if it doesn't exist:
    ```bash
    kubectl create namespace vault-server
    ```
    *Note: Also ensure the `vault-tls` secret (containing `vault.ca`, `vault.crt`, `vault.key`) and the `k8s-cephfs` StorageClass exist in this namespace before proceeding.*

3.  **Install Vault using Helm:**
    Deploy Vault using the Helm chart and your custom values file. Make sure you are in the directory containing the `Vault` folder or adjust the path to `-f Vault/my-values.yaml` accordingly.
    ```bash
    helm install vault hashicorp/vault --namespace vault-server -f Vault/my-values.yaml
    ```
    This command installs Vault into the `vault-server` namespace using the configurations specified in `Vault/my-values.yaml`.

4.  **Initialize Vault & Save Keys:**
    Once the `vault-0` pod is running and ready, initialize Vault. This generates the master keys and the initial root token, outputting them in JSON format.
    *   Exec into the `vault-0` pod and save the JSON output to a file named `vault-init-keys.json` in your current directory:
        ```bash
        kubectl exec --namespace vault-server -it vault-0 -- vault operator init \
            -key-shares=5 \
            -key-threshold=3 \
            -format=json > vault-init-keys.json
        ```
    *   **IMPORTANT:** Securely store the `vault-init-keys.json` file. It contains the Unseal Keys and the Initial Root Token required for unsealing and initial authentication. **Losing this file means losing access to your Vault data.** You will need to extract the keys from this file for the next step.

5.  **Unseal Vault:**
    Vault starts in a sealed state. You need to provide the unseal keys (from the `vault-init-keys.json` file generated in the previous step) to make it operational. You must provide 3 different keys out of the 5 generated keys.
    *   Extract three different unseal keys from the `unseal_keys_b64` or `unseal_keys_hex` array within your `vault-init-keys.json` file.
    *   Run the following command three times, replacing `<unseal-key-from-json>` with a different unseal key each time:
        ```bash
        kubectl exec --namespace vault-server -it vault-0 -- vault operator unseal <unseal-key-from-json>
        ```
    *   After providing the third valid key, Vault should become unsealed and ready to use. You can check the status:
        ```bash
        kubectl exec --namespace vault-server -it vault-0 -- vault status
        ```
        Look for `Sealed: false`.

## Accessing Vault UI

Based on your `my-values.yaml`, the Vault UI should be accessible via NodePort on port `30820`. Find the IP address of one of your Kubernetes nodes and access the UI in your browser at `https://<node-ip>:30820`.

You will need the Initial Root Token (found as `root_token` in the `vault-init-keys.json` file) to log in for the first time.
