vsetv.com-grabber
=================

##English
A tv guide grabber from vsetv.com. Script grabs tv guide in xmltv for one day.

##Dependecies
* python2.7 and above
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)

##Usage
You should have an account on vsetv.com if you want your own tv guide.
The script created as cli utility. It has four arguments:

`-h, --help` show help message and exit  
`-u`          vsetv.com user  
`-p`          vsetv.com password  
`-o`          output file, if omitted the script saves result in tv_guide.xml


##Русский
Граббер сайта vsetv.com. Извлекает программу телепередач на один день в формате xmltv.

##Зависимости
* python2.7 и выше
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)

##Использование
Необходимо иметь учётную запись на vsetv.com, чтобы составить свою программу передач.
Скрипт работает как утилита командной строки. Имеются четыре ключа:

`-h, --help`  показать справку и выйти  
`-u`          vsetv.com логин  
`-p`          vsetv.com пароль  
`-o`          выходной файл, если не указан, то скрипт сохраняет в файл с именем tv_guide.xml