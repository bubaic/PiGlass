echo "Shutting down"
python -c "__import__("piglass").setStopped(True)"
sleep 3s
sudo shutdown now -h
