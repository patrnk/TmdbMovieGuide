# TMDB Movie Guide
The repository consists of the scripts that work with [TMDB](https://www.themoviedb.org/)'s API.

The interface of the scripts is in Russian.

The scripts require Python 3.5 to run. Some of them require the user to have a working v.3 API key obtained from TMDB.
### movies_budget.py
The script retrieves movie's budget. Example usage:
```#!bash
$ python3 movie_budget.py 215 b000b0000d0bf0ac00000a000006e000
Бюджет фильма "Пила 2" составляет 4000000 долларов.
```
Here, 215 is the id of the movie on TMDB, and b000b0000d0bf0ac00000a000006e000 is an v.3 API key.
### download_db.py
The script retrieves various info about random movies and saves it into a file. Note that in order to comply with the EULA you should delete the files in a couple of days. 
Example usage:
```#!bash
$ python3 download_db.py 1000 test.json b000b0000d0bf0ac00000a000006e000
Скачиваем идентификаторы...
Узнаем подробности...
Записываем в json-файл...
Готово!
```
Here, 1000 is the number of movies to save in a test.json file. b000b0000d0bf0ac00000a000006e000 is an v.3 API key.

The script may take a long time to execute.
### search_db.py
The script retrieves finds all movie titles with the parameter as a substring. 
Example usage:
```#!bash
$ python3 search_db.py "пил" test.json
Результаты:
Пила 2
Скотт Пилигрим против всех
Пила. Игра на выживание
Готово!
```
Here, "пил" is the substring to search and test.json is a json file retrieved with download_db.py.
