#!/usr/bin/env bash
# Program:
#       This program is install Calamari-aler service on your server.
# History:
# 2015/11/24 Kyle.Bai <kyle.b@inwinstack.com> Release


for SERVICE in calamari_alert
do
sudo useradd --home-dir "/var/lib/${SERVICE}" \
--create-home \
--system \
--shell /bin/false \
${SERVICE}

# Create essential dirs

sudo mkdir -p /var/log/${SERVICE}
sudo mkdir -p /etc/${SERVICE}

# Set ownership of the dirs

sudo chown -R ${SERVICE}:${SERVICE} /var/log/${SERVICE}
sudo chown -R ${SERVICE}:${SERVICE} /var/lib/${SERVICE}
sudo chown ${SERVICE}:${SERVICE} /etc/${SERVICE}
done

function install_alert(){
    echo "Installing ...."
}


function uninstall_alert(){
    echo "Uninstalling ...."
}


