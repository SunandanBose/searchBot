# Search BOT

### To run the app do
```
./setup.sh

# Create db
curl -X 'POST' \
  'http://localhost:8000/createDB/' \
  -H 'accept: application/json' \
  -d ''
```


### Start application on laptop start
- Update SearchBOT_startup_Script.plist and setup.sh
- copy the file to ```/Library/LaunchDaemons/```
- execute below comands
```
sudo chown root:wheel /Library/LaunchDaemons/SearchBOT_startup_Script.plist
sudo chmod 644 /Library/LaunchDaemons/SearchBOT_startup_Script.plist
sudo launchctl load /Library/LaunchDaemons/SearchBOT_startup_Script.plist
launchctl start SearchBOT_startup_Script
```
