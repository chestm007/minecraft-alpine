# mincreft-alpine : Minecraft Server on Alpine Linux


comes packaged with fabric, fabric-carpet, carpet-extra, and carpet-autocrafting

versions supported:

- 1.14.4
- 1.15.2
- 1.16
- 1.16.1
- 1.16.2
- 1.16.3
- 1.16.4
- 1.16.5
- 1.17
- 1.17.1
- 1.18
- 1.18.1

## Build

``` sh
./build $MC_VERSION
```

## Build including better minecraft modpack

``` sh
./build $MC_VERSION bmc
```

## Run
loads data directories (example directory is in mc_config) from /srv/docker_volumes/minecraft-$MC_VERSION

```
./launch_container $MC_VERSION
```

## Options
* Port assignment: `-p HOST_PORT:CONTAINER_PORT`
* Volume mounting: `-v HOST_DIR:CONTAINER_DIR`
* \# of Threads for GC: `-e GCTHREADS=4` (default: `1`)
* Selecting version: `-e VERSION=1.7.3` (default: `latest-release`)
	* If you specified `latest-release` or `latest-snapshot`, a program will be automatically updated whenever this image starts.
* Specifying a jar file: `-e EXEC_JAR=forge-1.7.10-10.13.4.1614-1.7.10-universal.jar` (default: latest version of program)
	* If you specify this, you should download a jar manually and [add it to a container](https://docs.docker.com/engine/reference/commandline/cp/) or place it on a mountpoint to /srv/minecraft.
* Heap size: `-e MAX_HEAP=2048M` (default: `1024M`), `-e MIN_HEAP=512M` (default: `512M`)
* To detach : `Ctrl-p Ctrl-q` (if you created a container with -i option)
