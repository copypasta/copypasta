COPYPASTA README

CopyPasta is an online clipboard that can be used to store random bits of text.
The website automatically scales for mobile devices and easy-of-use is one of the
top functionality requirements.

Rquirements:

-Ubuntu or most linux distro
-Python 2.7 or greater (http://www.python.org/)
-web.py framework 0.37 or latest version (http://webpy.org/)
-SQlite 2.8 or greater (http://sqlite.org/)

You can download the source code from https://github.com/copypasta/copypasta.

Run instructions:

To run copypasta, run the 'python pasta.py' in a terminal:

notroot@ubuntu:~/copypasta$ ls
CopyPasta_doc_appsec.doc  model.pyc  pasta.pyc     README.md   sessions  static     users.sqlite
model.py                  pasta.py   pasta.sqlite  schema.sql  source    templates
notroot@ubuntu:~/copypasta$ python pasta.py
http://0.0.0.0:8080/

You can then just launch a browser and point to http://localhost:8080/
