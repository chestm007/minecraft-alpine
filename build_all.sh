VERSIONS=`cat README.markdown | grep '\- ' | cut -d ' ' -f 2`

echo $VERSIONS | xargs -l /bin/sh build.sh