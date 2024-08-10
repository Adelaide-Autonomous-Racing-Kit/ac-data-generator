docker run --rm \
    -it \
    --shm-size 80G \
    -v /media/james/JimmyB/work/aarc/:/data/ \
    -v /media/james/JimmyB/work/aarc/tracks:/tracks/ \
    -v /home/james/Documents/generated:/out/ \
    -e CONFIG_PATH='nordschleife.yaml' \
    ac-data-generator