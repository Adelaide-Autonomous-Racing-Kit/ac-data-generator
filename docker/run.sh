docker run --rm \
    --shm-size 80G \
    -v /mnt/data/aarc/recordings/:/data/ \
    -v /mnt/data/aarc/tracks:/tracks/ \
    -v /home/james/Documents/generated:/out/ \
    -e CONFIG_PATH='vallelunga.yaml' \
    ac-data-generator