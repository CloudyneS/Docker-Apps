set -e && \
echo "Starting to chown..." && \
chown -R nobody:root /app || true && \
echo "Finished chown!" && \
sudo -u nobody -E /usr/bin/python3 /init-py/init.py