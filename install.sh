#!/bin/bash

# install orcale-java8
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get -y update
sudo apt-get -y install oracle-java8-installer

# do the following if oracle java8 fails to install
# cd /var/lib/dpkg/info
# sudo sed -i 's|JAVA_VERSION=8u181|JAVA_VERSION=8u191|' oracle-java8-installer.*
# sudo sed -i 's|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u181-b13/96a7b8442fe848ef90c96a2fad6ed6d1/|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u191-b12/2787e4a523244c269598db4e85c51e0c/|' oracle-java8-installer.*
# sudo sed -i 's|SHA256SUM_TGZ="1845567095bfbfebd42ed0d09397939796d05456290fb20a83c476ba09f991d3"|SHA256SUM_TGZ="53c29507e2405a7ffdbba627e6d64856089b094867479edc5ede4105c1da0d65"|' oracle-java8-installer.*
# sudo sed -i 's|J_DIR=jdk1.8.0_181|J_DIR=jdk1.8.0_191|' oracle-java8-installer.*

# install cassandra
echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
sudo apt-get -y update
sudo apt-get -y install cassandra

# install required modules
pip install -r requirements.txt
pip install cassandra-driver --install-option="--no-cython"

# enable and start cassandra service and wait for 30 seconds
sudo service cassandra start
sleep 30

# create Keyspace and add admin credentials
python db_create.py
