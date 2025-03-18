# GitLab Runner Installation Guide

## Prerequisites
- Docker installed on your system
- Access to GitLab instance
- Runner registration token
- SSL certificate (if using HTTPS)

## Installation Steps

1. **Run GitLab Runner Container**
   ```bash
   docker run -d \
     --name gitlab-runner \
     --add-host "gitlab.brizo.me:10.192.127.229" \
     --restart always \
     -v /srv/gitlab-runner/config:/etc/gitlab-runner \
     -v /var/run/docker.sock:/var/run/docker.sock \
     gitlab/gitlab-runner:latest
   ```

2. **Set up SSL Certificate**
   ```bash
   # Create SSL directory
   mkdir -p /srv/gitlab-runner/config/ssl/

   # Copy GitLab CA certificate
   cp /path/to/gitlab-brizo-ca.crt /srv/gitlab-runner/config/ssl/gitlab-brizo-ca.crt
   ```

3. **Register the Runner**
   ```bash
   gitlab-runner register \
     --url https://gitlab.brizo.me \
     --token glrt-t1_Q6TDsh4rPJLJ9fwqZyfd \
     --tls-ca-file /etc/gitlab-runner/ssl/gitlab-brizo-ca.crt
   ```

4. **Complete Interactive Registration**
   - Follow the interactive prompts:
     1. Enter the executor type (e.g., docker, shell, etc.)
     2. Choose the default Docker image (if using Docker executor)
     3. Set any additional tags or options
     4. Confirm the registration

## Verification
- Check runner status: `docker ps | grep gitlab-runner`
- Verify registration in GitLab UI under CI/CD Settings

## Notes
- Ensure proper network connectivity to GitLab instance
- Keep the registration token secure
- Make sure SSL certificates are properly configured if using HTTPS

5. **Modify Runner Configuration**
   - Edit the `/srv/gitlab-runner/config/config.toml` file:
     ```toml
     [[runners]]
       [runners.docker]
         pull_policy = "if-not-present"
         extra_hosts = ["gitlab.brizo.me:10.192.127.229", "registry.okcs.com:10.192.30.201"] #for any extra-host
         privileged = true
         image = "docker:24.0.5"
         volumes = ["/var/cache/apk"] # Use a volume for local cache
     ```

6. **Restart gitlab-runner container**
   ```bash
   docker container restart gitlab-runner
   ```