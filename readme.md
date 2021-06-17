# task12  

---  
постановка задачи (автоматизация ручной работы):  
в каждом офисе есть локальный СКУД (магнитный замок, контроллер, приложение с локальной БД)
необходимо обьеденить все офисы для единого управления СКУД и одной БД сотрудников  

---  

в документации есть упоминание о возможности использования вместо локальной БД - БД MSQL
при множественном подключение к каждому контроллеру упоминается "сервер JAVA" (заготовка из "установленого клиента под Windows")

---
идея:  
1) установить обьеденяющий "java-сервер" на linux  
2) установить общую БД MSQL на linux  
3) конфигурация локальных СКУД (клиентское приложение под Windows)  

реализация и тестирование:  
(1) - установка "службой" для автоматического запуска после старта/перезагрузки  
(2) - от разработчика есть приложение для импорта-експорта localDB-mysqDB, Microsoft SQL Server Management Studio 18  

баги:  
- через периодические проблемы с сетью "java-сервер" становился недоступным (служба оставалась запущеной, без ошибок)  
    решение: создание в планировщике задачи перезапуска "java-сервер" каждый час (более чем за 6 месяцев жалоб не поступало)  
    */60 * * * * sudo service partizan restart  
        - через 2 месяца обнаружено "заполнение" дискового пространства "логами"  
            решение: изменить bash для запуска (добавлена очистка "tmp" перед запуском)  

            rm -fr /tmp/jetty*  

---  
``` 
встановлення і налаштування доступу до Ubuntu Server 18.04 (ssh, port, etc.)

копіювання ключів ssh (первинне)
sudo apt update
sudo apt install openssh-server
cat ~/.ssh/id_rsa.pub | ssh <user>@<hostname> "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
sudo systemctl disable --now ssh
sudo systemctl enable --now ssh
часовий пояс
sudo timedatectl list-timezones
sudo timedatectl set-timezone Europe/Kiev
sudo reboot


копіювання на сервер "заготовки" (вмісту папки "partizan") і надання відповідних прав
    /partizan
scp -r partizan <user>@<hostname>:
cd /home/user/partizan
sudo chmod o+w AX*

встановлення SQL
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/18.04/mssql-server-2019.list)"
sudo apt-get update
sudo apt-get install -y mssql-server
sudo /opt/mssql/bin/mssql-conf setup
systemctl status mssql-server --no-pager

curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update 
sudo apt-get install mssql-tools unixodbc-dev
sudo apt-get update 
sudo apt-get install mssql-tools
    
sqlcmd -S localhost -U SA -P '<YourPassword>'

підключення пустої БД із "заготовки" через Microsoft SQL Server Management Studio 18 (connect...->Databases->Attach...->Add...->AXData.MDF (/home/user/partizan))

встановлення Java
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre
/partizan/bin/./server.sh
ip_partizan:8089
admin/admin
зміна паролю!!!
налаштування порту (/partizan/lib/config.txt стандарт 8089)

налаштування автозапуску сервісу
1)sudo nano /etc/systemd/system/partizan.service
[Unit]
Description = Server PartizanACM
After=multi-user.target
[Service]
Type=idle
ExecStart=/home/user/partizan/start
[Install]
WantedBy=multi-user.target
2)sudo chmod 644 /etc/systemd/system/partizan.service
cd /etc/systemd/system/
sudo systemctl enable partizan.service
3)sudo nano /home/user/partizan/start
#!/bin/sh
cd /home/user/partizan/bin
./server.sh
4)sudo chmod u+x /home/user/partizan/start

5) для зміни порту ssh
nano /etc/ssh/sshd_config
Port 22 -> Port 25622

6) були випадки “зависання” сервісу JAVA - вирішено шляхом перезавантаження сервісу (робота контролерів в офісах не блокується) 
sudo crontab -e
*/60 * * * * sudo service partizan restart

```  
