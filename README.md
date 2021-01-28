## CCT (Covid Contact Tracing) Library
### With Firebase database and proximity detection modules for Micropython

This repo contains a library coded and organized for students participating in a high school STEM competition. Students will use the library to build an an automated Covid contact tracing application for an ESP32 microcontroller kept attacked to their ID tags.

Many of the Micropython modules come from third-party code: see [Credits](#Credits).

### Instructions

#### Setting up development environment

- First, download the most recent library release, with a filename like `cct-release-<version.zip`, from:  https://github.com/esbullington/cct/releases/latest
- Unzip the zip file.
- Open up Windows Powershell ISE as admin (type "powershell ise" in Windows search box, then "Run as Administrator")
- In the bottom window of the Windows Powershell ISE, enter at the prompt (`PS C:\Windows\system32 >`) the following:

```powershell
Set-ExecutionPolicy Bypass -Scope Process
```

- Access the execution policy change with "Yes to All"
- Then, using the `file` menu, or the open folder icon, navigate to the unzipped zip file, then to the `tools` subfolder
- Double-click on the `install.ps1` file
- Now, click the "run script" button (green play icon) to run the script and install project environment

### Running code on the ESP32

To run the ESP32 environment, run the following command. Set `--editor` flag to whichever editor you wish to use (to use Visual Studio Code, use `--editor code`):

```bash
rshell -p <COM3 or whichever serial port the board is on> -b 115200 --editor code
```

Now that you're in the rshell environment, you can start the Python prompt inside the ESP32 device by running the `repl` command. To start the editor, run `edit <yourfiletoedit.py>`. To view the ESP32 filesystem, navigate to the board using the command `cd /pyboard` (and `ls` to list files). You should also view the other commands that are available using the `help` command.


### Firebase setup + authentication

To be able to removely connect to the Google Firebase API, you'll need to create a service account. Follow these directions up until you are able to download the JSON key (you'll use the same type of key to connect as to a Google Sheet):

https://denisluiz.medium.com/python-with-google-sheets-service-account-step-by-step-8f74c26ed28e

No need to use the Python code at the end of that page, since this project uses Firebase and Micropython instead of the Google Sheets and regular Python shown there.

Make sure to note the email of your Service Account you create, and save the downloaded JSON credential key, since you'll need both of those two connect to either the Firebase database.

Be sure to use the same project that you created above when you make a Firebase database. If you're just using the Firebase database, there's no need to create a spreadsheet and give permissions to the service account created above.

#### Converting the PKCS1 key to a format that can be loaded on the ESP32
Run `tools/extract.sh <yourdownloadedjsonkey.json> key.json` on a Linux, Mac, or Windows WSL, and save the `key.json` at the root of the ESP32 filesystem.

### Firebase database creation

Go to the [Firebase database console](https://console.firebase.google.com/u/0/). Click `Add project` button. On the next screen, be sure to select the same project you created while setting up your Service Account. Click on `Realtime database` and note the name of the database in the center of the screen (create one if there is not one there).

### Documentation

#### Project library documentation

Find `cct` library documentation at: https://esbullington.github.io/cct/index.html

#### Micropython documentation

- [General documentation](https://docs.micropython.org/en/latest/index.html)

- [Special ESP32 Micropython functionalities](https://docs.micropython.org/en/latest/esp32/quickref.html)

### Credits

The modules `google.auth`, `ntp`, `wifi` from (or based on) [esp32-weather-google-sheets](https://github.com/artem-smotrakov/esp32-weather-google-sheets) by Artem Smotrakov, licensed under MIT.

The code in `google.rsa` is a Micropython port by Artem Smotrakov of the original Python `rsa` package, which was written by Sybren A. Stuvel and licensed under the Apache Software License (ASL 2).

All other modules by Eric S Bullington and licensed under MIT.


### Todo

- Change getter and setter methods to properties
- Library documentation

### License

#### General library code

MIT License

Copyright (c) 2020 Artem Smotrakov, Eric S Bullington

#### `google.rsa`:

Copyright (c) Sybren A. Stuvel, Artem Smotrakov

Apache Software License (ASL 2)
