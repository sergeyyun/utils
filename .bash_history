sudo dpkg-reconfigure tzdata
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6 --assume-yes
sudo ln -s /usr/bin/python3.6 /usr/bin/python
sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
sudo apt-get upgrade --assume-yes
sudo apt-get install build-essential unzip --assume-yes
sudo apt-get install python3-setuptools python3-dev --assume-yes
sudo apt-get install git-core --assume-yes
sudo su
curl https://raw.githubusercontent.com/aurora/rmate/master/rmate > rmate
sudo mv rmate /usr/local/bin
sudo chmod +x /usr/local/bin/rmate
rmate ~/.bashrc
source ~/.bashrc
rmate ~/.bashrc
source ~/.bashrc
mkdir /home/ubuntu/mpcs
cd /home/ubuntu/mpcs
mkvirtualenv mpcs
pip install --upgrade boto3
pip install --upgrade jmespath-terminal
pip install --upgrade awscli
pip install --upgrade PyMySQL
pip install --upgrade psycopg2-binary
pip install --upgrade sqlalchemy
pip install --upgrade stripe
pip install --upgrade flask
pip install --upgrade flask-sqlalchemy
pip install --upgrade gunicorn
pip install --upgrade globus_sdk
workon mpcs
deactivate
workon mpcs
python
cd
deactivate
ll
ll .ssh
sudo adduser --disabled-password --gecos ‘mpcsroot' mpcsroot
sudo adduser --disabled-password --gecos 'mpcsroot' mpcsroot
sudo bash -c '/bin/echo campusadmin ALL=\(ALL:ALL\) NOPASSWD:ALL >> /etc/sudoers'
sudo mkdir /home/mpcsroot/.ssh
sudo nano /home/mpcsroot/.ssh/authorized_keys
sudo chmod 600 /home/mpcsroot/.ssh/authorized_keys
sudo chown -R mpcsroot:mpcsroot /home/mpcsroot/.ssh
ll
chmod 755 .ssh
ll
ll .ssh
workon mpcs
git clone https://github.com/mpcs-cc/gas.git
ll
cd gas
ll
nano .env
./run_gas_prod.sh 
cat run_gas_prod.sh 
nano run_gas_prod.sh 
./run_gas_prod.sh 
./run_gas_prod.sh console
python
sudo netstat -tupan
g, endpoint_bridge)
python
cat /home/ubuntu/.ssh/authorized_keys 
ll
ll ssl
ll /usr
ll /usr/local
ll /usr/local/sr
ll /usr/local/src
mkdir /usr/local/src/ssl
sudo mkdir /usr/local/src/ssl
sudo mv ssl/ /usr/local/src/ssl/
ll
ll /usr/local
ll /usr/local/src
ll /usr/local/src/ssl/
cd /usr/local/src/ssl
sudo mv ssl/* .
ll
rmdir ssl
sudo rmdir ssl
cd
ll
cd gas
rmate run_gas_prod.sh 
./run_gas_prod.sh 
./run_gas_prod.sh console
ll /usr/local/src/ssl
sudo chmod 400 /usr/local/src/ssl/*
./run_gas_prod.sh 
cat log/gas.log 
cd ..
git clone https://github.com/mpcs-cc/anntools.git
cd anntools/
ll
rmate config.txt 
ll data
cat run.py 
python run.py data/test/vcf
python run.py /home/ubuntu/anntools/data/test/vcf
python run.py /home/ubuntu/anntools/data/test.vcf
ll
cd data
ll
cd ..
rm -rf data
cat config.txt 
cd ..
rm -rf anntools/
git clone https://github.com/mpcs-cc/anntools.git
cd anntools/
nano config.txt 
ll
cd ..
mkdir util
ll
cd gas
ll
cat run_gas_prod.sh 
cd ..
rm -rf gas
nano .ssh/authorized_keys 
sudo shutdown -h now
cd gas
ll
nano .ssh/authorized_keys 
sudo shutdown -h now
ll
ll /var/log
nano /var/log/cloud-init-output.log 
nano /var/log/cloud-init.log 
nano /var/log/cloud-init-output.log 
ll
cd anntools/
workon mpcs
python
python manage db inti
python manage db init
cd ..
git clone https://github.com/mpcs-cc/gas-framework.git /home/ubuntu/gas
cd gas
python manage db init
ll
python manage.py db init
cd ..
pip install --upgrade pip
pip install --upgrade flask_migrate
pip install --upgrade flask_script
cat .ssh/authorized_keys 
nano .ssh/authorized_keys 
cat .ssh/authorized_keys 
ll
rm -rf gas
ll
sudo shutdown -h now
ll
ll /var/lib
ll /var/lib/cloud
ll /var/lib/cloud/data
ll /var/lib/cloud/scripts/
ll /var/lib/cloud/scripts/per-once
ll /var/lib/cloud/scripts/per-boot
ll /var/lib/cloud/scripts/per-instance
tailf /var/log/cloud-init-output.log
ll
sudo rm -rf /var/lib/cloud/*
sudo shutdown -h now
ls
rm -r -f anntools
rm -r -f util
ls
workon mpcs
echo "" > util.py
rmate util.py
mv util.py results_notify.py
ls
rmate results_notify.py
python results_notify.py
rmate results_notify.py
workon mpcs
ls
git init
git remote add origin https://github.com/sergeyyun/utils.git
git add .
git remove .
git rm .
git rm -r *
ls
git commit -m "first commit"
git push origin master
ls
python results_notify.py
rmate results_notify.py
python results_notify.py
ls
workon mpcs
python results_notify.py
echo "" > results_archive.py
rmate results_archive.pt
rmate results_archive.py
ls
rmate results_notify.py
python results_notify.py
python results_archive.py
ls
python results_archive.py
git status
git add .
git commit -m '7 done'
git push origin master
workon mpcs
rmate results_archive.py
workon mpcs
ls
python results_archive.py
rmate results_archive.py
python results_archive.py
rmate results_archive.py
python results_archive.py
git add .
git commit -m '8 done'
git push origin master
python results_archive.py
workon mpcs
python results_archive.py
rmate results_archive.py
python results_archive.py
ls
echo "" > archive_restore.py
rmate archive_restore.py
rmate results_archive.py
python results_archive.py
ls
python archive_restore.py
python archive_restore.py [A
python archive_restore.py
python results_archive.py
rmate results_archive.py
python results_archive.py
rmate results_archive.py
rmate archive_restore.py
python results_archive.py
workon mpcs
ls
python results_notify.py
git add .
git commit -m 'bug fixing'
python results_notify.py
ls
git status
git add .
git commit -m '1-9 done'
git push origin master
python results_notify.py
python archive_restore.py
workon mpcs
python archive_restore.py
