#!/bin/sh
set -e -x -m

mount_dir=/opt/minecraft

function slink {
  echo linking $1
  ln -s $1 /srv/minecraft/
}

function slink_d {
  # symlink a directory if it exists, otherwise create it
  if [ -d "$1" ]; then
    slink $1
  else
    rm -rf "/srv/minecraft/$(echo $1 | cut -d '/' -f 4)"
    mkdir $1
    slink $1
  fi
}

function slink_f {
  # symlink a file if it exists
  if [ -f "$1" ]; then
    slink $1
  else
    echo "WARN: cannot find file {$1}"
  fi
}

slink_d "${mount_dir}/logs"
slink_d "${mount_dir}/world"
slink_d "${mount_dir}/resourcepacks"
slink_d "${mount_dir}/texturepacks"

slink_f "${mount_dir}/banned-ips.json"
slink_f "${mount_dir}/banned-players.json"
slink_f "${mount_dir}/ops.json"
slink_f "${mount_dir}/server.properties"
slink_f "${mount_dir}/usercache.json"
slink_f "${mount_dir}/whitelist.json"

FIFO=mcfifo

: ${MAX_HEAP:="1024M"}
: ${MIN_HEAP:="512M"}
: ${GCTHREADS:="2"}
: ${JAVA_PARAMS:=-Xmx${MAX_HEAP} -Xms${MIN_HEAP} -XX:ParallelGCThreads=${GCTHREADS}}

echo "eula=true" >> eula.txt

rm -f "$FIFO"
mkfifo "$FIFO"

trap 'echo "Received a signal, server will stop soon."; echo "stop" > "$FIFO";' HUP INT QUIT TERM

tail -n1 -f "$FIFO" | /usr/bin/java ${JAVA_PARAMS} -jar "/srv/minecraft/fabric-server-launch.jar" nogui &
mc_pid=$!

wait $mc_pid
echo "Server stopped."

exit 0

# vim: set ts=4 sw=4 :
