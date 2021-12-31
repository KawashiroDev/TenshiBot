#pycord update script, updates the dev version for slash commands and stuff
echo updating pycord...
#go to server root dir
cd ..
cd ..
#clone latest pycord
git clone https://github.com/Pycord-Development/pycord
#go into dir
cd pycord
#install
python3 -m pip install -U .[voice]
#exit dir
cd ..
#delete dir
echo cleaning up...
rm -r pycord
#restart Tenshi
echo restarting Tenshi
cd TenshiBot
pkill Tenshi
python3 Tenshi.py

