set -e

docker pull alpine

DOCKER_IMAGE=quay.io/chestm007/alpine-base

echo $DOCKER_IMAGE

# DO THE ROAR
echo 'building...'
docker build -t $DOCKER_IMAGE --quiet --rm=true .
echo 'pushing...'
docker push ${DOCKER_IMAGE}
