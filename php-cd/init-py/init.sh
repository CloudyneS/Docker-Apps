set -e && \
export COMPOSER_HOME="/etc/composer" && \
mkdir /tmp/app && \
echo "Starting to chown..." && \
chown -R unit:root /app /tmp/app || true && \
chmod -R 770 /tmp/app && \
echo "Finished chown!" && \
sudo -u unit -E /usr/bin/python3 /init-py/init.py