#!/usr/bin/env bash
# Program:
#       This program is install Calamari-aler service on your server.
# History:
# 2015/11/24 Kyle.Bai <kyle.b@inwinstack.com> Release


for SERVICE in calamari
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

sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y python-setuptools python-pip libpq-dev python-dev libmysqlclient-dev libxml2-dev libxslt1-dev

function install_alert(){
    echo "Installing ...."
    sudo python setup.py install
    sudo cp -r scripts/calamari-alert.conf /etc/init/
    sudo cp -r etc/calamari/calamari-alert.conf /etc/calamari/
}


function uninstall_alert(){
    echo "Uninstalling ...."
    sudo pip uninstall calamari-alert
    sudo rm /etc/init/calamari-alert.conf
    sudo rm /etc/calamari/calamari-alert.conf
}

read -p "Install/Uninstall(Yes/No)：" check

if [ ${check} == 'Yes' ] || [ ${check} == 'yes' ]; then
    if pip list | grep -Fxq "calamari-alert"
    then
        echo "calamari alert service is installed ..."
    else
        install_alert
    fi
elif [ ${check} == 'No' ] || [ ${check} == 'no' ]; then
    if pip list | grep -Fxq "calamari-alert"
    then
        uninstall_alert
    else
        echo "calamari alert apis is uninstalled ..."
    fi
else
    echo "ERROR Input......"
fi