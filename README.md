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
