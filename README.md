![GitHub License](https://img.shields.io/github/license/mjbaeidi/Brizo)

# Brizo

Welcom to Brizo Project. This is going to be a **Fully Automated CI-CD Pipeline**


## This is Roadmap of this project

1. - [X] Upgrade Docker using Ansible
2. - [X] Install k8s
3. - [X] Back-end Storage k8s (cephfs)
4. - [X] Install FreeIPA
5. - [X] Install Gitlab Server
     > 1. full install with Local Agent using Docker
     > 2. Integerate with LDAP freeipa
6. - [X] Prepare python API code with Docker file & Image
7. - [X] write k8s Manifests
8. - [X] Use Ingress (Use GatewayAPI of kubernetes and Traefik)
9. - [X] Install Image Repository (use already existed jfrog)
10. - [X] Design Gitlab PipeLine (some parts deploy for testing purpose)
    > 1. Pull
    > 2. Test
    > 3. Build
    > 4. Scan Image
    > 5. Push
    > 6. Deploy (Test)
    > 7. Deploy (Production)
11. - [X] Install ArgoCD (use add on microk8s)
12. - [X] Integrate Different Parts
13. - [X] monitoring (the app use APM of elastic which has been configured already )
14. - [X] Install Rancher or better Dashboard (portainer)
