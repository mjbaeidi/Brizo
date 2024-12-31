# Guide to Installing GitLab

Follow these steps to install GitLab:

1. Create the GitLab directory:

   ```sh
   sudo mkdir -p /srv/gitlab
   ```
2. Set the `GITLAB_HOME` environment variable:

   ```sh
   export GITLAB_HOME=/srv/gitlab
   ```
3. Append the `GITLAB_HOME` environment variable to your shell’s profile:

   ```sh
   echo 'export GITLAB_HOME=/srv/gitlab' >> ~/.bashrc
   source ~/.bashrc
   ```
4. Generate the CA private key and certificate:

    ```sh
    openssl genrsa -out ca.key 4096

    openssl req -x509 -new -nodes -sha512 -days 3650 \
    -subj "/OU=Personal/CN=gitlab.brizo.me" \
    -key ca.key \
    -out ca.crt
    ```

5. Generate the GitLab private key and certificate signing request (CSR):

    ```sh
    openssl genrsa -out gitlab.brizo.me.key 4096

    openssl req -sha512 -new \
    -subj "/OU=Personal/CN=gitlab.brizo.me" \
    -key gitlab.brizo.me.key \
    -out gitlab.brizo.me.csr
    ```

6. Create the `v3.ext` file for the certificate extensions:

    ```sh
    cat > v3.ext <<-EOF
    authorityKeyIdentifier=keyid,issuer
    basicConstraints=CA:FALSE
    keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
    extendedKeyUsage = serverAuth
    subjectAltName = @alt_names

    [alt_names]
    DNS.1=gitlab.brizo.me
    DNS.2=gitlab.brizo
    EOF
    ```

7. Generate the GitLab SSL certificate:

    ```sh
    openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in gitlab.brizo.me.csr \
    -out gitlab.brizo.me.crt
    ```

8. Add the GitLab SSL certificate and key to the GitLab configuration:

    ```sh
    cp gitlab.brizo.me.crt $GITLAB_HOME/config/ssl/
    cp gitlab.brizo.me.key $GITLAB_HOME/config/ssl/
    ```

9. Use Docker Compose to bring up GitLab:

   ```sh
   docker-compose up -d
   ```
