Python script for working SIGUR access control system.

- web_serv_delegation.py - if recieved allow from db send to sigur controller over SIGUR programm installed on server or work station OS Windows or Linux.
- web_serv_event.py - recieved event data from sigur and record data in db.
- settings.ini - configuration file for connection to data base MS SQL.

for start script require:
python3.6
Ubuntu Server 18.04 LTS and user with sudo right
and type commands:
```
mkdir /home/user/my_project
cd /home/user/my_project
sudo apt update
sudo apt install unixodbc-dev
sudo apt install g++
python3.6 venv env
source env/bin/activate
pip install wheel
pip install -r requirements.txt
```

