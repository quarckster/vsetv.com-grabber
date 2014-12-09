vsetv.com-grabber
=================

Граббер сайта vsetv.com. Извлекает программу телепередач на один день в формате xmltv.

#Зависимости
* python2.7
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)

#Использование
Необходимо иметь учётную запись на vsetv.com, чтобы составить свою программу передач.
Для логина на сайт скрипт использует данные из cookie, а именно атрибуты "cll" и "cp".
Скопируйте эти значения в строку `self.g.setup(cookies={"cll":"your_cookie", "cp":"your_cookie"})`.