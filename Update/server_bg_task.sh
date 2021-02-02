echo Server update script
#run debian update commands
apt-get update -y
apt-get upgrade -y
#update python packages
python3.5 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
#kill and restart remote access
service ssh stop
service xrdp stop

service ssh start
service xrdp start
#cleanup server space using bleachbit 
bleachbit --clean --preset
