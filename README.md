# Calamari Alert Service 
本服務為 Calamri Alert Service 監控套件，會在指定作業系統底下提供一個 Calamari 的 Alert Service，來提供儲存系統的錯誤訊息，該服務應以 Python 撰寫且可獨立運作，即可能不運作於 Calamari 伺服器。當儲存系統發生錯誤時，該服務須執行之功能包含：
* 寫入警告紀錄至資料庫
* 寫入系統日誌 (Syslog)
* 發送電子郵件

Installation
------------
首先安裝 Python pip 套件：
```sh
$ sudo apt-get install -y git python-pip
```
從 Git Server 將套件的 Repositiory 下載至安裝的本機端上：
```sh
$ git clone https://github.com/inwinstack/calamari-alerting.git
$ cd calamari-alerting
```

之後安裝相關環境套件：
```sh
$ sudo apt-get update 
$ sudo apt-get install postgresql-contrib python-setuptools libpq-dev python-dev libmysqlclient-dev libxml2-dev libxslt1-dev -y 
```

安裝資料庫系統，這邊採用 Postgresql：(Option)
```sh
$ sudo apt-get install postgresql 
```

修改預設 User 密碼，這邊範例使用 Postgresql，若已有存在資料庫，則不用該步驟：(Option)
```sh
$ sudo -u postgres psql postgres
$ \password postgres
$ \q
```
> 在執行上個步驟若出現”psql: could not connect to server: No such file or directory
Is the server running locally and accepting
connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?

> 可以執行以下步驟來解決，以 postgresql 9.3 為例：
```sh
$ LC_ALL=C sudo pg_createcluster 9.3 main ; sudo /etc/init.d/postgresql restart
```


建立一個名稱為```calamari-alert```的使用者：
```sh
$ SERVICE="calamari-alert"
$ sudo useradd --home-dir "/var/lib/${SERVICE}" --create-home --system --shell /bin/false ${SERVICE}
```

建立 log 與 conf 目錄，並複製 conf 檔案到 etc 底下：
```sh
$ sudo mkdir -p /var/log/${SERVICE}
$ sudo mkdir -p /var/run/${SERVICE}
$ sudo mkdir -p /etc/${SERVICE}
$ sudo chown -R ${SERVICE}:${SERVICE} /var/log/${SERVICE}
$ sudo chown -R ${SERVICE}:${SERVICE} /var/run/${SERVICE}
$ sudo chown -R ${SERVICE}:${SERVICE} /etc/${SERVICE}
$ sudo cp -r etc/calamari-alert/calamari-alert.conf /etc/${SERVICE}/
```

安裝```calamari-alert```服務套件：
```sh
$ sudo python setup.py install
```

編輯```/etc/calamari-alert/calamari-alert.conf```檔案，並修改一下：
```sh
[DEFAULT]
debug = True

log_format = %(asctime)s %(levelname)-5s [%(name)s] - "%(message)s"
log_date_format = %Y-%m-%d %H:%M:%S
log_dir = /var/log/calamari-alert

[ssl]
verify = False
ca_file_dir = /var/lib/calamari-alert/ssl
ca_files = apache.crt, apache.key

[calamari]
url = http://calamari.example.com
port = 80
username = example
password = example

[database]
# Example:
# MySQL: connection = mysql://root:calamari@192.168.99.100/calamari
# Postgresql: connection = postgresql://postgres:calamari@192.168.99.100/calamari
connection = postgresql://calamari:27HbZwr*g@192.168.99.100/calamari

[email]
address = smtp.gmail.com
port = 587

# The 'mode' is setting smtp security, Two options 'None' and 'TLS'
mode = TLS
username = example@gmail.com
password = example
```
> 若使用```HTTPS```的話，請在```[ssl]```部分設定驗證的金鑰與目錄，或者透過設定```verify```來忽略驗證。


複製```scripts/calamari-alert-service```到```/etc/init.d```底下：
```sh
$ sudo cp -r scripts/calamari-alert-service /etc/init.d/
$ sudo chmod 775 /etc/init.d/calamari-alert-service
```
完成檔案複製後，使用 update-rc.d 指令設定開機啟動：
```sh
$ sudo update-rc.d calamari-alert-service defaults
```

啟動服務：
```sh
$ sudo service calamari-alert-service start
* Starting ceph calamari-alert service ...                                                                                [ OK ]
```
> Debug 可以使用```sudo service calamari-alert-service systemd-start```。

License
-------