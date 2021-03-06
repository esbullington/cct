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
- Close Powershell ISE

#### Setting up Visual Studio Code

In the step above, the program Visual Studio Code, which we'll abbreviate VSCode, was installed on your computer. This is the program -- called an IDE (Integrated Development Environment) -- we'll use to program the ESP32. Open up VSCode, and select "Open folder" under the `file` menu. Navigate to the `cct-release...` folder that you created above by unzipping the project zip file. Be sure to open the nested `cct-release...` folder if Windows created two of them (eg, `C:\Users\johndoe\Downloads\cct-release-0.2.4\cct-release-0.2.4`). The folder you want to open file contain subfolders such as `board`, `tools`, `firmware`, etc.

Once that folder has been opened, a few necessary extensions may start to install. Once they're installed, your development environment should be ready to use.

#### Setting up the ESP32 on Windows

To communicate with the ESP32, and to run code on the device, we need to make sure the ESP32 is properly set up on Windows. Often, when you first plug the device in, Windows will automatically install any needed drivers. So plug the device into the USB port, and watch for a "Setting up device..." prompt (you may need to click "yes" if prompted to install any drivers).

After the drivers are installed, open up the Windows Device Manager by typing "device manager" in the search box and clicking on the Windows Device Manager prompt. Check under the "Ports" entry to see if the device is listed as "USB Serial Port (COM3)" (it's possible it will be another COM number).  If the entry displays an exclamation mark, right click on the entry and select "Update driver". 

Once the device is shown without any exclamation point warning symbols, it should be ready to be programmed. But first, you'll need to flash the device with Micropython firmware to be able to use Python to program the ESP32.

#### Flashing the ESP32 firmware with Micropython

In order to run Python code on the ESP32, we first we have to flash the device with the Micropython firmware:

- Open up Visual Studio Code
- Under the `Terminal` top menu, select `Run Task`
- Under `Run Task`, select `Flash Initial Firmware`
- Enter your port number (probably "COM3")
- It will take a while to flash the firmware, be sure not to disconnect the ESP32 while it's flashing the device 
- Once you see the words "Hash of data verified.", then your ESP32 has bee properly flashed. You may now press any key to close the terminal.

### Running code on the ESP32

To run Python on the ESP32 environment, you have two choices: you can either do your development on Windows, and then copy the files onto the ESP32, or you can edit the files directly on the device (there's actually an intermediate file created, but it will seem as though you're working directly on the device). But first, you have to do an initial deployment of the library files we'll use:

#### Deploying library code

Under the `terminal` menu, select `Run task` just as you did above when flashing the ESP32, but this time, select `Deploy updates to ESP32 (All files)`. This option deploys the Micropython library we'll be using to connect to wifi, write to a remote Firebase database, and interact with the Bluetooth device from our downloaded, unzipped code folder, to the ESP32. **This will take a while to deploy (5-10 minutes)**. Once that's done,  you can proceed to either interacting with the ESP32 using the prompt (REPL), or editing and deploying your code to the device.

#### Micropython REPL Prompt

<todo>

#### Editing code on Windows

Edit code in Visual Studio Code just as you would in any other editor. You will do your work in the `main.py` file under the `board` directory. When you're ready to run the code:

- Under the `Terminal` top menu, select `Run Task`
- Under `Run Task`, select `Deploy Updates to ESP32`
- Enter your port number (probably "COM3")

#### Editing code on the device
run the following command. Set `--editor` flag to whichever editor you wish to use (to use Visual Studio Code, use `--editor code`):

```bash
rshell -p COM3 -b 115200 --editor code
```

If your board is on another serial port than `COM3`, use that port instead. You can find out which port the board is on by viewing the device under the Window's device manager. You may need to update device drivers if your device shows an exclamation point in the device manager panel.

Now that you're in the rshell environment, you can start the Python prompt inside the ESP32 device by running the `repl` command.

To start the editor and edit files directly on the board, run `edit <yourfiletoedit.py>`.

To view the ESP32 filesystem, navigate to the board using the command `cd /pyboard` (and `ls` to list files).

You should also run `help` to view the other commands that are available (eg, `rsync` syncing files on the board with the Windows machine).

### Firebase setup + authentication

To be able to remotely connect to the Google Firebase API, you'll need to create a service account. Follow these directions up until you are able to download the JSON key (you'll use the same type of key to connect as to a Google Sheet):

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
