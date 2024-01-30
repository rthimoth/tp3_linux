Avoir python 3.11 ainsi que pip pour installer des packets 

```
git clone https://github.com/rthimoth/tp3_linux.git
```

```
pip3 install psutil
```

Création du service Check

monit.service

```
sudo nano /etc/systemd/system/monit.service


[Unit]
Description=monit service

[Service]
ExecStart=/home/ranvin/tp3_linux/monit.py check
User=ranvin
Group=ranvin

[Install]
WantedBy=multi-user.target
```

Création du service timer qui permet de lancer le programme toutes les heures
```
monit.timer


sudo nano /etc/systemd/system/monit.timer   

[Unit]
Description=Timer pour le service monit

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h

[Install]
WantedBy=timers.target
```

```
sudo chmod +x /home/ranvin/tp3_linux/log

sudo chmod +x /home/ranvin/tp3_linux/log/monit.log

sudo chmod +x /home/ranvin/tp3_linux/monit
```

```
sudo chown -R ranvin:ranvin home/ranvin/tp3_linux/log

sudo chown -R ranvin:ranvin home/ranvin/tp3_linux/log/monit.log

sudo chown -R ranvin:ranvin home/ranvin/tp3_linux/monit

sudo systemctl daemon-reload

sudo systemctl enable monit.service

sudo systemctl start monit.service
```

toutes les commandes possible dans le programme monit.py

permet de recupèrer toutes les données du monitoring

```
python3 monit.py check 
```

permet de recupèrer le derniers rapport
```
python3 monit.py get last 
```

liste tout les rapports

```
python3 monit.py list
```

fait un pourcentage sur l'utilisation des ram et du cpu

```
python .\monit.py get avg 3
```


permet de t'aider si tu n'arrives pas a utiliser le programme
```
python3 monit.py -h
```

lancer l'api avec 

```
python3 api1.py
```

acceder en localhost à l'api avec la liste de tout les rapports

