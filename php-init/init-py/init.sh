set -e && \
chown -R nobody:root /app || true && \
sudo -u nobody -E /usr/bin/python /init-py/init.py