#! /usr/bin/bash
sudo pip install requests beautifulsoup4
sudo cp 'loadshedding.py' '/usr/local/bin/loadshedding'
rm '$HOME/.loadshedding.routine' -f
echo 'Successfull installed!'
