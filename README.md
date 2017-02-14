# TMDB Movie Guide
The repository consists of the scripts that work with [TMDB](https://www.themoviedb.org/)'s API. For thorough description of how to use a particular script, run the script with -h option.

The scripts require Python 3.5 to run. Some of them require the user to have a working v.3 API key obtained from TMDB.
### budget.py
The script retrieves movie's budget. Example usage:
```#!bash
$ python3 budget.py 215
TMDB API key:
The budget of the movie 'Saw II' is $4000000.
```
Here, 215 is the id of the movie on TMDB. 
### fetch.py
The script retrieves various info about random movies and saves it into a file. Note that in order to comply with the EULA you should delete the files in a couple of days. 
Example usage:
```#!bash
$ python3 fetch.py 1000 -o test.json
TMDB API key:
test.json already exists. Rewrite? [y/n]: y
Downloading ids...
Getting additional info...
Writing to a json-file...
Done!
```
Here, 1000 is the number of movies to save in a test.json file. In this case, the file already exist, but we decide to overwrite it. By default everything is saved into movies.json.

This script may take a long time to execute.
### search.py
The script retrieves finds all movie titles with the parameter as a substring. 
Example usage:
```#!bash
$ python3 search.py 'xxx' -i test.json
Results:
xXx: Return of Xander Cage
```
Here, 'xxx' is the substring to search and test.json is a json file retrieved with fetch.py (by default, it's 'movie.json').
### recommend.py
The script suggests a list of movies to watch based on the movie title provided. The movie must be in a database.
Example usage:
```#!bash
$ python3 recommend.py 'xXx: Return of Xander Cage' --top 3 --infile test.json
Recommendations:
Jurassic World
Suicide Squad
Interstellar
```
Here, 'xXx: Return of Xander Cage' is the movie upon which the suggestions are based. '3' is the number of suggested movies and 'test.json' is a json file retrieved with fetch.py (again, it's 'movies.json' by default).
# Purpose
This is a homework assignment for styleru_py course.
