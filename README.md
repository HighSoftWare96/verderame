# verderame
DontLetYourVegetablesDie!

## Deploy on rasbperry

For the deploy on the Raspberry device:

- The Rasberry device is visible online through a service called [Ngrok](https://dashboard.ngrok.com/get-started/setup/raspberrypi)
- There is a small server (`deploy/syncServer.py`) that accepts requests on `POST /webhook :5000`
- On valid requests the servers pulls the content of this repository on the branch `main` (or otherwise the specified one in the args) and restart the systemd service related to this project
- Github is configured to call the small server with WebHooks each time some code is pushed

