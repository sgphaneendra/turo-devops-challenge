# Turo Devops Challange

- have used nginx as the webserver of choice.
- bash scripting was used to create the build script that build and pushes docker image.
- Python script was used to update the tag version in terraform code and create PR.
- Github actions is used to create the CI/CD Pipeline
- have covered all the enhancements.
- Have made a slight change in enhancement 3 due to time constraints. The requirement was to populate index page with value from config map set as environment variable. That required templating static pages and rendering them with values from configmap. instead populated the entire index page from config map content writted to html file mounted as volume.

  ## Docker build script

  - Dockerfile with nginx base image is created to run nginx app with custom static pages in docker container.

  ```bash
  $ ./build.sh <docker_user> <docker_pwd>
  ```

  - this script builds and pushed docker image to dokcer hub with git short commit id used as tag value. It also outputs the tag value with image name.
  - github actions pipeline `build.yml` used this script to build and push docker image.
  - When any change is made to the repo this pipeline is triggered.
 
  ## Terrafrom & K8S

  - terraform code is created to deploy the applicaiton to kubernetes cluster.
  - kubeconfig is configured in the kubernetes provider config so that it reads kubeconfig file from local and connects to the cluster.
  - kubernetes manifest files are in `terraform/k8s` folder.

  ```bash
  $ cd terraform
  $ terraform init
  $ terraform plan
  $ terraform apply --auto-approve
  ```

  - terraform uses aws s3 bucket as remote backend to manage state.
  - Kubernetes objects like pods, deployments, services, configmaps, ingress with sub domain url and certificates provided are created.
  - The application is accessible at `https://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/`
 
  ## Application endpoints

  - `/` serves index page
   ```
    curl https://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/
    <html>
    <h1>Index Page from configmap!</h1>
    </br>
    </html>
  ```
  - `/index.html` serves index page
   ```
    curl https://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/index.html
    <html>
    <h1>Index Page from configmap!</h1>
    </br>
    </html>
  ```
  - `/page1.html` gets redirected and serves `page2.html`
   ```
    curl -v https://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/page1.html
    *   Trying 34.237.96.10:443...
    * Connected to phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu (34.237.96.10) port 443 (#0)
    > GET /page1.html HTTP/1.1
    > Host: phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu
    > User-Agent: curl/7.81.0
    > Accept: */*
    > 
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 301 Moved Permanently
    < Server: nginx/1.23.0
    < Date: Thu, 15 Feb 2024 23:02:33 GMT
    < Content-Type: text/html
    < Content-Length: 169
    < Connection: keep-alive
    < location: http://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/page2.html
    <html>
    <head><title>301 Moved Permanently</title></head>
    <body>
    <center><h1>301 Moved Permanently</h1></center>
    <hr><center>nginx/1.25.4</center>
    </body>
    </html>
    * Connection #0 to host phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu left intact
    ```
  - `config.html` serves page populated from k8s configmap 
    ```
    curl https://phaneendra.test-subaccount-1-v02.test-subaccount-1.rr.mu/config.html
    <html>
    <h1>Configmap Page!</h1>
    </br>
    </html>
    ```
  ## CI CD Flow

  - When feature branch is created and changes made build pipeline is created and new docker image is created and pushed.
  - `Update tag` pipeline can be manually triggered with image tag version passed as workflow input. Python deployment script creats a new release branch, updates terraform.tfvars.json file with new tag, commits and pushes and creates a ne Pull Request.
  - When pull request is merged to main branch, `deploy` pipeline is triggered which deploys the laytest image to K8S cluster by running terraform apply.
