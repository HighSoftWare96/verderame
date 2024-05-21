# verderame
DontLetYourVegetablesDie!

## Deploy on rasbperry

For the deploy on the Raspberry device:

- The Rasberry device port 5000 will be visible online through a service called [Ngrok](https://dashboard.ngrok.com/get-started/setup/raspberrypi)
- There is a small server (`deploy/syncServer.py`) that accepts requests on `POST /webhook :5000`
- On valid requests the servers pulls the content of this repository on the branch `main` (or otherwise the specified one in the args) and restart the systemd service related to this project
- Github is configured to call the small server with WebHooks each time some code is pushed

## First installation

- Setup your ngrok account and obtain an API token
- Clone repository on your device in `$HOME/verderame`
- Fix your environment inside `verderame/.env` (add user password!)
- Run `NGROK_APP_TOKEN={YOUR_TOKEN} pipenv run install`

The syncServer should be running as systemd service `verderame-syncer`, this service will sync automatically the just cloned repository and restart the systemd service `verderame` that is the actual application.

