vsetv.com-grabber
=================

##English
A tv guide grabber from vsetv.com. Script grabs tv guide in xmltv for one day.

##Dependecies
* python2.7
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)

##Usage
You should have an account on vsetv.com if you want your own tv guide.
This script use cookies for login, in particulary fields "cli" и "cp".
Just copy these values in line `self.g.setup(cookies={"cll":"your_cookie", "cp":"your_cookie"})`.

##Русский
Граббер сайта vsetv.com. Извлекает программу телепередач на один день в формате xmltv.

##Зависимости
* python2.7
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)

##Использование
Необходимо иметь учётную запись на vsetv.com, чтобы составить свою программу передач.
Для логина на сайт скрипт использует данные из cookie, а именно атрибуты "cll" и "cp".
Скопируйте эти значения в строку `self.g.setup(cookies={"cll":"your_cookie", "cp":"your_cookie"})`.