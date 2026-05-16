# Docker & Docker Compose Cheat Sheet

## Docker Commands
* `docker build -t app_name .` : Build an image from a Dockerfile
* `docker images` : List all images
* `docker run -d -p 8000:8000 app_name` : Run container in detached mode mapping port 8000
* `docker ps` : View running containers
* `docker stop <container_id>` : Stop a running container
* `docker rm <container_id>` : Remove a container

## Docker Compose Commands
* `docker-compose up -d` : Start all services in detached mode
* `docker-compose up --build -d` : Rebuild images and start services
* `docker-compose down` : Stop and remove containers, networks, and default volumes
* `docker-compose logs -f` : View and follow logs for all services
