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

If it is the first time you are using `contact`, please be sure to initialize the database with the `reset` command
```
contact reset
```

## Usage

## License


