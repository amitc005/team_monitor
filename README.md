# Team Monitor Application

## Setup Development Environment

### Clone the source repository and initialize the code.

1. Cloning this repository using git.
   ```bash
   git clone https://github.com/Texada/srm_rest_api.git
   ```

### Run the dev environment with Docker.

1. Please refer [Docker Install Doc](https://docs.docker.com/install/) to install the docker

2. Run the docker image via the docker-compose.
   ```bash
   docker-compose up -d --build
   ```
3. Open browser <http://127.0.0.1:8000/swagger/>. Need to wait for the server is ready.
4. To see the docker logs to run the following command.
   ```bash
   docker logs team_monitor_web_1
   ```

### Run development server

1. On Ubuntu system, install the underlying linux packages before installing the python dependencies.
   ```bash
   sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
   ```
2. Create a virtual environment

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Make virtual enviorment using pip
   ```bash
   pip install -r docker/requirements.txt
   ```
4. Run development server
   ```bash
   flask run
   ```
5. Open browser <http://127.0.0.1:8000/swagger/>
