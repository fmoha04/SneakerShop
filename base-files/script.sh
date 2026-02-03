#!/bin/bash
for i in `cat $1`
do
  adduser $i
  mkdir -p /home/$i/.kube
  cp /root/.kube/config /home/$i/.kube/config
  chown -R $i:$i /home/$i/.kube
  chmod 600 /home/$i/.kube/config
done
