FROM alpine
MAINTAINER Max Chesterfield

ARG exec_user=minecraft
ARG mount_dir=/opt/minecraft
ARG server_dir=/srv/minecraft

USER root
RUN apk --update add openjdk17-jre jq curl \
	    && addgroup -g 1000 ${exec_user} \
	    && adduser -H -D -G ${exec_user} -u 1000 ${exec_user} \
	    && mkdir -p ${server_dir} \
	    && mkdir -p ${mount_dir} \
	    && chown ${exec_user}:${exec_user} ${server_dir}

# Minecraft Port
EXPOSE 25565


# exec program
#USER ${exec_user}
STOPSIGNAL TERM
ENTRYPOINT ["/usr/local/bin/minecraft_launcher.sh"]
