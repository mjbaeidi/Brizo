# Guide to Installing Freeipa

> **Note:** Before starting the steps, ensure you have the following setting in your Docker configuration:
> 
> ```json
> {
>     "userns-remap": "default"
> }
> ```

1. Use the `freeipa.yml` compose file and run the command in detach mode:

   ```sh
   docker-compose -f freeipa.yml up -d
   ```
2. Attach a tty session into the created container:

   ```sh
   docker exec -it <container_name> /bin/bash
   ```
3. Fill in the required sections as prompted.
4. Use web access to complete the setup by navigating to the FreeIPA web interface.