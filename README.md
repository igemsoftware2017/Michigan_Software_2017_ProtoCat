# ProtoCat - Protocol Database Software by Michigan Software 2016

If you would like to avoid the hassle of installing your own version of Protocat, simply go to [protocat.org](protocat.org) for our version on the web.

If you have are planning to run this on a Ubuntu development computer, you must install additional packages in order to get the Pip package Pillow. To do this, enter into your terminal:
```
sudo apt-get install python-dev
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```
Next, you must have Python 2.7, 3.4, or 3.5 installed on your computer and accessible on the terminal as well as pip (may be already installed when you installed Python). This software comes default on Ubuntu and Mac, but on Windows you must get an installation from the [Python website](https://www.python.org/downloads/release/python-350/).
Then, install Django 1.9 or 1.10, Pillow, djangorestframework, drfdocs, and bleach through the command on Linux:

```
sudo pip install django Pillow djangorestframework drfdocs bleach
```

Or on Windows:

```
pip install django Pillow djangorestframework drfdocs bleach
```

Then, to install our software, if you have git installed on your computer, simply type

```
git clone https://github.com/igemsoftware2016/Michigan16.git
```

Otherwise, you can go to the [GitHub page](https://github.com/igemsoftware2016/Michigan16) and click download there.

Now, open up a terminal/command prompt and go into the newly downloaded folder (default name Michigan16) and type in the follow:
```
cd mibiosoft
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
Then, use your preferred browser and in the address bar and type [localhost:8000](localhost:8000), and then your should see a local version of ProtoCat running on your own computer.
