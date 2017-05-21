vsetv.com-grabber
=================

## English
A tv guide grabber from vsetv.com. This script grabs a tv guide in xmltv format for one or more days.

## Dependecies
* python3
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)
* transliterate

## Usage
You should have an account on vsetv.com if you want your own tv guide.
The script created as cli utility. Available keys:

`-h, --help` show help message and exit  
`-u`          vsetv.com user  
`-p`          vsetv.com password  
`-o`          output file, if omitted the script saves result in tv_guide.xml  
`-d`          number of days with EPG (one day by default)  
`--stdout`	  output to stdout


## Русский
Граббер сайта vsetv.com. Извлекает программу телепередач на один и более дней в формате xmltv.

## Зависимости
* python3
* Grab (http://grablib.org/)
* xmltv (https://bitbucket.org/jfunk/python-xmltv)
* transliterate

## Использование
Необходимо иметь учётную запись на vsetv.com, чтобы составить свою программу передач.
Скрипт работает как утилита командной строки. Ключи:

`-h, --help`  показать справку и выйти  
`-u`          vsetv.com логин  
`-p`          vsetv.com пароль  
`-o`          выходной файл, если не указан, то скрипт сохраняет в файл с именем tv_guide.xml  
`-d`          количество дней (значение по умолчанию один день)  
`--stdout`	  итоговый xml отправить на стандартный вывод