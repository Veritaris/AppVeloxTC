cd AppVeloxTC
git pull
pip3 install -r requirements.txt
pip3 install coveralls
COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN coveralls
sudo service nginx reload
sudo service unit restart