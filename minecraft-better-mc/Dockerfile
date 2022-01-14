ARG mc_version
FROM quay.io/chestm007/minecraft-alpine:${mc_version}
ARG FABRIC_LOADER_VERSION
ARG FABRIC_INSTALLER_VERSION
MAINTAINER Max Chesterfield


ARG server_dir=/srv/minecraft
WORKDIR ${server_dir}
COPY temp_dir/mods/* ${server_dir}/mods/
COPY temp_dir/config ${server_dir}/config
COPY temp_dir/kubejs ${server_dir}/kubejs
COPY temp_dir/fabric-installer/* ${server_dir}
