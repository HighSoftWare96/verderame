curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok
ngrok config add-authtoken $NGROK_APP_TOKEN


sudo cp ./systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable verderame-syncer.service
sudo systemctl enable verderame.service
sudo systemctl start verderame-syncer.service
sudo systemctl start verderame.service
sudo systemctl status verderame-syncer.service
sudo systemctl status verderame.service

ngrok http http://localhost:5000