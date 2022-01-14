set -e

echo "building $1"
rm -rf temp_dir
mkdir temp_dir
mkdir temp_dir/mods
mkdir temp_dir/config
mkdir temp_dir/kubejs
mkdir temp_dir/fabric-installer
touch temp_dir/fabric-installer/dummyfile

USER_SPECIFIED_VERSION=$1
BASE_IMAGE=quay.io/chestm007/minecraft-alpine:$USER_SPECIFIED_VERSION

echo 'updating base image'
docker pull $BASE_IMAGE

echo 'install better mc'
python better_mc_version.py $USER_SPECIFIED_VERSION

if [[ $USER_SPECIFIED_VERSION == '1.17.1' ]]; then
  echo "downloading fabric..."
  FABRIC_INSTALLER_VERSION=0.7.1
  FABRIC_LOADER_VERSION=0.11.7
  echo $FABRIC_INSTALLER_VERSION
  cd temp_dir
  wget -q -O fabric-installer.jar https://maven.fabricmc.net/net/fabricmc/fabric-installer/$FABRIC_INSTALLER_VERSION/fabric-installer-$FABRIC_INSTALLER_VERSION.jar
  java -jar fabric-installer.jar server -loader 0.11.7 -mcversion 1.17.1 -dir fabric-installer
  cd -
  cp -r ../assets/better_mc/$USER_SPECIFIED_VERSION/kubejs/* temp_dir/kubejs/
fi

DOCKER_IMAGE=$BASE_IMAGE-bmc

DOCKER_BUILDKIT=1

# DO THE ROAR
echo 'building...'
docker build --build-arg mc_version=$USER_SPECIFIED_VERSION -t $DOCKER_IMAGE .
echo 'pushing...'
docker push ${DOCKER_IMAGE}
