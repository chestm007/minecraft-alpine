sudo rm -rf $PWD/mc_config/world/*
sudo rm -rf $PWD/mc_config/logs
echo "autoCraftingTable true" > $PWD/mc_config/world/carpet.conf
docker pull quay.io/chestm007/minecraft-alpine:$1
/usr/bin/docker run --rm -t --rm --name=minecraft-server \
           		              -p 25565:25565 \
           		              -e MAX_HEAP=6G \
                            -v $PWD/mc_config:/opt/minecraft \
                            -v /etc/localtime:/etc/localtime:ro \
                            quay.io/chestm007/minecraft-alpine:$1