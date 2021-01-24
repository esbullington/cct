## CCT (Covid Contact Tracing) Library
### With Firebase database and proximity detection modules for Micropython

This repo contains a library organized and built for students participating in a high school STEM competition. Students will use the library to build an an automated Covid contact tracing application for an ESP32 microcontroller kept attacked to their ID tags.

### Instructions

#### Setting up development environment

- First, you need to make sure you have a (regular) Python 3 environment on Windows. Specifically, you need to have access to the `pip` command to install Python packages, which we'll have to use to install the tools needed to flash the Micropython onto the esp32, and then the tools needed to interact with it. This should make both the `python3` and the `pip3` commands available on the command line. Python 3 can be downloaded from: https://www.python.org/downloads/

- You also will need to install OpenSSL, can be found below the [`curl` download links here](https://curl.se/windows/). Look for the `OpenSSL <version> [64bit/32bit]` (probably you'll want the 64bit version). After you've downloaded it, make sure you've added the path to the Windows Environment path, so that the `openssl` command is available on the Windows command line.

- Using the `pip` (or maybe `pip3`) command on the Windows command line, install the `rsa` package:

```
pip install rsa
```

#### Setting up environment for ESP32

- Using the `pip` (or maybe `pip3`) command on the Windows command line from above, you need to install the `esptool` and `rshell` packages:

```
pip install esptool
pip install rshell
```

- To run the ESP32 environment, run the following command. Set `--editor` flag to whichever edit you wish to use (for instructions on how to use Visual Studio Code, see instructions under [Editor](#editor) below):

```
rshell -p <serial port here: eg, `COM5`> -b 115200 --editor vim
```

- Now that you're in the `rshell` environment, you can start the Python prompt inside the ESP32 device by running the `repl` command. To start the editor, run `edit <yourfiletoedit.py>`.

### Editor

- Download Visual Studio Code:
    - https://visualstudio.microsoft.com/downloads/

- Download the Python extension for VSCode, and Intellisense:
    - https://marketplace.visualstudio.com/items?itemName=ms-python.python
    - https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode

- Follow instructions (here)[https://github.com/Josverl/micropython-stubber] to install autocompletion and code linting for Micropython

- Make sure that the visual studio `code` command is on the Windows command line path

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
