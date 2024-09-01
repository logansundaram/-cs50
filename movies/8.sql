SELECT name FROM people JOIN stars JOIN movies WHERE people.id = stars.person_id AND stars.movie_id = movies.id AND movies.title = 'Toy Story';
