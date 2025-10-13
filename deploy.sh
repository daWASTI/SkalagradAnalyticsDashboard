docker stop skalagrad-analytics || true
docker rm skalagrad-analytics || true
docker rmi dawasti/skalagrad-analytics:latest || true
docker build . -t dawasti/skalagrad-analytics:latest
docker run -d -p 8050:8050 --name skalagrad-analytics --restart always --cpus=1 --memory=1000m dawasti/skalagrad-analytics:latest