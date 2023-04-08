docker run --rm \
    --shm-size 80G \
    -v /home/james/Documents/:/mnt \
    -e CONFIG_PATH='monza.yaml' \
    -u $(id -u):$(id -g) \
    ac-data-generator