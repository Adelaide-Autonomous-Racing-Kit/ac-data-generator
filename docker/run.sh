docker run --rm \
    --shm-size 80G \
    -v /mnt/data:/data \
    -v /home/james/Documents/generated:/out/ \
    -e CONFIG_PATH='spa.yaml' \
    ac-data-generator