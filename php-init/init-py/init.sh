set -e && \
chown -R nobody:root /app || true && \
sudo -u nobody -E /usr/bin/python3 /init-py/init.py