echo "PiGlass Installation Procedure"
echo "Updating Package Cache"
sudo apt-get update
echo "Installing updates"
sudo apt-get upgrade -y
echo "Installing dependancies"
sudo apt-get install python python-pygame python-pyaudio xserver-xorg xinit xserver-xorg-video-fbdev xserver-xorg-video-vesa wicd dhclient wicd-curses nano flac -y
echo "Dependancies Installed"
echo "Creating user"

echo "User Created"
echo "Setting options"

echo "Options set"
echo "Install done, launching"
cd /home/piglass/ && python start.py
