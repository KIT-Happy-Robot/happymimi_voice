#!/bin/bash
#roslaunch respeaker_ros respeaker.launch
net=$(iwgetid -r)
if [ "$net" = "KIT-WLAP2" ]; then
  export https_proxy=http://wwwproxy.kanazawa-it.ac.jp:8080/
  export http_proxy=http://wwwproxy.kanazawa-it.ac.jp:8080/               
  echo "Changed https_proxy for GCP API"
else
  export https_proxy=''
  export http_proxy=''
  echo "Cleared http_proxy and https_proxy"
fi

source ~/catkin_ws/src/ggi/env/bin/activate
#gnome-terminal -- python
#gnome-terminal --load-config=~/.bashrc 

roslaunch spr_speak spr_speak.launch
