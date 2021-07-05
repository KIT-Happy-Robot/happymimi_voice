#!/bin/sh

#学内proxyを経由するかどうか確認
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

#仮想環境へ入る
source ~/catkin_ws/src/voice_reference/api/bin/activate

#launchファイルを起動
roslaunch voice_common_pkg sp_ggi.launch
