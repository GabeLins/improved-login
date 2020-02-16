# Login System
An improved version of my very first code.

## About
Less than a year ago, I started my journey in the world of programming. I have started this journey by watching some Python tutorials made by a YouTube channel called Curso em Video, where I've learned the basics but didn't keep watching the videos because I've chosen to learn on my own.

My first project was a simple (and stupid) login system where the only way of adding a new user was by changing the source and attaching a new if-else block. 

This repository contains my very first code and its improved version, made using a lot of things I've learned in the past months.

## Instructions

Setting up this repository is very simple.

To use this project, you need to install the requirements and run the app script:
```bash
$ pip install -r requirements.txt
$ python app.py
```
The script will set up the database, generate a secret key, and an SSL certificate and encryption key. After creating the certificate, you'll have to install it on your computer to remove the trust warning.

During the process of generating the SSL certificate, the script will ask you for a Common Name, if you want to use a custom common name instead of the default localhost, you'll have to set it manually on your */etc/hosts* file, as stated in [this answer](https://stackoverflow.com/a/28290207/12204083) on Stack Overflow. 
Adding the *SERVER_NAME* setting is not needed, though.
