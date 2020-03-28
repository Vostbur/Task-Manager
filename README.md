Task-Manager
============
Система управления проектами для командной работы на Flask.

    In app.py:
    'DEBUG = True' for local test running on http://127.0.0.1:5000/ 
    'DEBUG = False' for running on http://0.0.0.0:5000/ 

              
Install systemd service
=======================
(on Raspberry Pi for example)
----------------------------- 

sudo nano /etc/systemd/system/Task-Manager.service


	[Unit]
	Description="Task-Manager"
	
	[Service]
	User=pi
	Group=pi
	WorkingDirectory=/home/pi/projects/Task-Manager/Task-Manager
	VIRTUAL_ENV=/home/pi/projects/Task-Manager/.venv
	Environment=PATH=$VIRTUAL_ENV/bin:$PATH
	ExecStart=/home/pi/projects/Task-Manager/.venv/bin/python app.py
	Restart=on-failure
	
	[Install]
	WantedBy=multi-user.target

Exec:

	sudo systemctl daemon-reload 
	sudo systemctl enable Task-Manager
	sudo systemctl start Task-Manager
	sudo systemctl status Task-Manager
 
