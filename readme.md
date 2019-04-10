**proof of concept**  use the google drive API to hack bulk conversion of docx files to pdf from command line by just uploading to drive and downloading as pdf (!!!), because that seriously seems like the only way to do it.  

**USAGE**: first, follow the instructions in the quickstart link below to authorize access to your google drive and get a credentials.json file.  (You'll note an incredibly paranoid .gitignore in this repo to make double-triple-extra sure that I don't accidentially uploade that MOFO.).  Requires pipenv and python 2.7ish.  then install the libraries with `pipenv install` and run with `pipenv run python quickstart.py` and you'll end up with a entire directory full of pdf files with the same name as the docx files in said directory.  The working directory needs to be the one with the token file (because I'm too lazy to store things in an env or something), but to convert the docs in a different directory to pdfs in that directory, pass it a relative or tilde pathname, e.g. `pipenv run python quickstart.py ~/Desktop/docstoconvert`.

Code almost entirely cribbed from google documentation with seriously like 2 lines changed, so, copyright google I guess or something?  whatever license they have for their docs is gonna be what license applies to this.

gdrive documentation I mashed together in extreme laziness:

- [google python quickstart](https://developers.google.com/drive/api/v3/quickstart/python) ---follow instructions there re: authorizing drive access and such in order to get credentials file.  (I'm using py2x here because last time I tried to use google's py3 library things went pear-shaped) (and see [this so](https://stackoverflow.com/questions/36173356/google-drive-api-download-files-python-no-files-downloaded) on actually using the streaming io stuff, which I at least never do)

- [priv scopes](https://developers.google.com/drive/api/v3/about-auth) (I'm using full drive access, if someone wanted to turn this into a real app it could probably work with application data folder or something)

- [uploading](https://developers.google.com/drive/api/v3/manage-uploads) 

- [downloading](https://developers.google.com/drive/api/v3/manage-downloads)

[original tirade about the impossibility of bulk conversion from docx to pdf](https://twitter.com/PaulGowder/status/1115724305311178752)

[tirade part 2](https://twitter.com/PaulGowder/status/1115811431247642624)
