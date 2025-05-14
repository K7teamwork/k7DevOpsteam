#!/bin/bash

source venv/bin/activate


/var/lib/jenkins/workspace/election-cicd/election

python3 manage.py makemigrations
python3 manage.py migrate

echo "Migrations applied successfully"

/var/lib/jenkins/workspace/election-cicd/

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"


sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "Gunicorn started successfully"

sudo systemctl status gunicorn
