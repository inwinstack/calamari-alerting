#!/usr/bin/env bash
# Program:
#       This program is install Calamari-aler service on your server.
# History:
# 2015/11/24 Kyle.Bai <kyle.b@inwinstack.com> Release

function install_alert(){
    SERVICE="calamari-alert"
    sudo useradd --home-dir "/var/lib/${SERVICE}" --create-home --system --shell /bin/false ${SERVICE}

    # Create essential dirs
    sudo mkdir -p /var/log/${SERVICE}
    sudo mkdir -p /etc/${SERVICE}

    # Set ownership of the dirs
    sudo chown -R ${SERVICE}:${SERVICE} /var/log/${SERVICE}
    sudo chown -R ${SERVICE}:${SERVICE} /var/lib/${SERVICE}
    sudo chown ${SERVICE}:${SERVICE} /etc/${SERVICE}

    sudo mkdir -p /var/log/${SERVICE}
    sudo mkdir -p /var/run/${SERVICE}
    sudo mkdir -p /etc/${SERVICE}
    sudo chown -R ${SERVICE}:${SERVICE} /var/log/${SERVICE}
    sudo chown -R ${SERVICE}:${SERVICE} /var/run/${SERVICE}
    sudo chown -R ${SERVICE}:${SERVICE} /etc/${SERVICE}
    sudo cp etc/calamari-alert/calamari-alert.conf /etc/${SERVICE}/
    sudo cp scripts/calamari-alert-service /etc/init.d/
    sudo chmod 775 /etc/init.d/calamari-alert-service
    sudo update-rc.d calamari-alert-service defaults
}

function uninstall_alert(){
    SERVICE="calamari-alert"

    sudo service calamari-alert-service stop
    sudo userdel ${SERVICE}
    sudo pip uninstall ${SERVICE}
    sudo update-rc.d calamari-alert-service disable

    sudo rm /etc/init.d/calamari-alert-service
    sudo rm /var/run/${SERVICE}
    sudo rm /etc/${SERVICE}
    sudo rm /var/lib/${SERVICE}
    sudo rm /etc/${SERVICE}/calamari-alert.conf
}

read -p "You want to install?(Yes/No)：" check

if [ ${check} == 'Yes' ] || [ ${check} == 'yes' ]; then
    if pip list | grep -Fxq "calamari-alert"
    then
        echo "calamari alert service is installed ..."
    else
        echo "Installing ...."
        install_alert
    fi
elif [ ${check} == 'No' ] || [ ${check} == 'no' ]; then
    if pip list | grep -Fxq "calamari-alert"
    then
        echo "Uninstalling ...."
        uninstall_alert
    else
        echo "calamari alert apis is uninstalled ..."
    fi
else
    echo "ERROR Input......"
fi