#!/bin/bash

#1 secretos
kubectl apply -f /home/vagrant/SneakerShop/k8s/secrets.yml

#2 volumenes
kubectl apply -f /home/vagrant/SneakerShop/k8s/pv_volume.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/pvc_volume.yml

#3 mariadb
kubectl apply -f /home/vagrant/SneakerShop/k8s/mariadb_configmap.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/mariadb_deployment.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/mariadb_service.yml

#4 python
kubectl apply -f /home/vagrant/SneakerShop/k8s/python_deployment.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/python_service.yml

#5 apache
kubectl apply -f /home/vagrant/SneakerShop/k8s/apache_deployment.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/apache_service.yml

#6 phpmyadmin
kubectl apply -f /home/vagrant/SneakerShop/k8s/phpmyadmin_deployment.yml
kubectl apply -f /home/vagrant/SneakerShop/k8s/phpmyadmin_service.yml
