docker run \
    --rm \
    --shm-size 80G \
    -v /mnt:/mnt \
    -env CONFIG_PATH='configs/monza.yaml' \
    ac-data-generator