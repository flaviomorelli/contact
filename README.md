# contact

## Description

A CLI-tool that makes it possible to add an manage contacts in a contact book. `contact` implements all the basic functionality of a contact book such as adding, updating, deleting, and looking up a contact. 

`contact` is a personal project to learn more about CLIs, SQL, and general software development skills such as writing documentation and using version control. 

## Installation

After downloading the source code, you have to create and activate a virtual environment. Then install the `click` package.  

``` 
python -m venv contact_book
source contact_book/bin/activate
pip install Click
```

To call `contact` directly from the terminal instead of `python contact.py`, you have to install the package. 
```
pip install --editable .
```
Further information on how to set up `click` can be found [here](https://click.palletsprojects.com/en/7.x/setuptools/).

Now you can call `contact` directly from the terminal!
```
contact new john adams 12345678
contact show
```

## Usage

### 1. Initializing the database
If it is the first time you are using `contact`, please be sure to initialize the database with the `reset` command
```
contact reset
```
To initialize the database with mock data run
```
python initialize.py
```

The default is 30 contacts, but you can change the default by passing an argument in the command line. 
```
python initialize.py 50
```

### 2. Adding a contact

To add a contact you need the name, surname, and phone number of the person. Note that name and surname will be capitalized independently of how you typed them in.  
```
contact add dana woodward 018784376
```
As an option, you can add an email address or a birthday by passing the `--email` (`-e`), and `--birthday` (`-b`) flags respectively. 

```
contact add michael williams 5446723 -e michael.williams@gmail.com -b 08-07-1982
```
Note that the format of the birthday is `dd-mm-yyyy`

### 3. Showing contacts
Show all saved contacts (name, surname and phone number only )
```
contact show
```
Use the `--all` (`-a`) flag to show all the fields in the contact book (e.g. email address and birthday).

### 4. Searching contacts
The `show` command can also be used to search for contacts. With the `--name` (`-n`) or `--surname`(`-s`) options, you can look for all the contacts that have a matching name or surname. Neither name nor surname are case sensitive.
```
contact show -n dana -a 
```

If you do not remember the whole name or surname of the contact, you can activate partial matching with the `--find` (`-f`) flag. 
```
contact show -n mich -a -f
```

### 5. Updating a contact
To update a contact, you need to type the full name and surname of the person. You can change the phone number with the `--phone`(`-p`) option, the email with the `--email`(`-e`) option, and the birthday with the `--birthday`(`-b`) option. Please note that the birthday is in `dd-mm-yyyy` format. If no options are passed, no changes will be made.
```
contact update michael williams -e m.williams@posteo.eu
```

### 6. Deleting a contact
To delete a name from the contact book, you have to type the full name and surname. If you do not remember the exact name or surname, use the `show` command. 
```
contact delete michael williams
``` 

### 7. Backup of the database
If you have a Dropbox account, you can backup your database:
```
contact backup
```
To activate the backup, you have to install the dropbox library in Python, and also to [create an App on Dropbox](https://www.dropbox.com/developers/documentation/python#tutorial). Please call your App `contact_cli`, to make sure it saves the database in the right folder. If there is already a file with the same name in your Dropbox, it will be overwritten by default.

You can create a text file in your CLI-folder (i.e. the folder of contact.py) called `access_token` that includes your private access token to your own Dropbox account. If you do not want to keep it as a text file, it is also possible to pass it as an option with `--token` (`-t`). 

## License

MIT License

Copyright (c) 2019 Flavio Morelli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


