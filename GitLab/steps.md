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
4. Use Docker Compose to bring up GitLab:

   ```sh
   docker-compose up -d
   ```
