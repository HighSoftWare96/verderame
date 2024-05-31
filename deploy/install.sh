curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok
ngrok config add-authtoken $NGROK_APP_TOKEN


chmod +x ./run.sh
chmod +x ./deploy/sync.sh

sudo cp ./deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable verderamen.service
sudo systemctl enable ngrok.service
sudo systemctl start verderamen.service
sudo systemctl start ngrok.service
sudo systemctl status verderamen.service
sudo systemctl status ngrok.service

echo "Your app is listening on $NGROK_STATIC_DOMAIN..."
