from itertools import chain
from collections import Counter
from itertools import islice
from django.db.models import Prefetch
from movies.models import Movies


class TopFavouriteGenres(object):
    """
    Utility class for computing the top N favorite genres from movie collections.

    Methods:
    - `top_n_genres(lst, n=3)`: Given a list of genres, returns a comma-separated string
      containing the top N genres based on frequency.

    - `top_favourite_genres_from_user_collection(collections, n=3)`: Given a queryset of user's
      collections, retrieves the genres of associated movies and returns the top N favorite genres.

    """

    @staticmethod
    def top_n_genres(lst, n=3):
        _dict = Counter(lst)
        sorted_dict = dict(sorted(_dict.items(), key=lambda x: x[1], reverse=True))
        genres = list(islice(sorted_dict.keys(), n))
        return ",".join(genres)

    def top_favourite_genres_from_user_movie_collection(self, collections, n=3):

        user_collections = collections.prefetch_related(
            Prefetch(
                "movies",
                queryset=Movies.objects.only("genres"),
                to_attr="movies_with_genres",
            )
        )
        # Iterate through each collection of the user
        genres_list = []
        for collection in user_collections:
            # append genres to a list
            for movie in collection.movies_with_genres:
                genres_list.append(
                    movie.genres.split(",")
                )  # movie.genres is a string, make it a list using split.
        genres_list = list(chain(*genres_list))  # flatten the list
        top_genres = self.top_n_genres(
            genres_list, n
        )  # this method return top n genres from the given genres list.

        return top_genres
