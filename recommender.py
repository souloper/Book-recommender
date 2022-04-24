import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix



def get_book_info(name,book_cleaned_pivot):
    for book in book_cleaned_pivot.index:
        if name in book.str.lower():
            return book



def recommend(name):
    books = pd.read_csv('dataset/books.csv')
    ratings = pd.read_csv('dataset/ratings.csv')



    books['original_publication_year'] = books['original_publication_year'].fillna(-1).apply(lambda x: int(x) if x != -1 else -1)


    ratings_rmv_duplicates = ratings.drop_duplicates()
    unwanted_users = ratings_rmv_duplicates.groupby('user_id')['user_id'].count()
    unwanted_users = unwanted_users[unwanted_users < 3]
    unwanted_ratings = ratings_rmv_duplicates[ratings_rmv_duplicates.user_id.isin(unwanted_users.index)]


    new_ratings = ratings_rmv_duplicates.drop(unwanted_ratings.index)
    new_ratings['title'] = books.set_index('id').title.loc[new_ratings.book_id].values


    cleaned_books=pd.merge(new_ratings,books,on='title')
    rating_count=(cleaned_books.
        groupby(by = ['title'])['rating'].
        count().
        reset_index().
        rename(columns = {'rating': 'totalRatingCount'}))


    book_with_totalRatingCount = cleaned_books.merge(rating_count, left_on = 'title', right_on = 'title', how = 'left')     
    columns = ['book_id_x','language_code','ratings_count','ratings_5','id','book_id_y','best_book_id','work_id','books_count','work_ratings_count','work_text_reviews_count','ratings_1','ratings_2','ratings_3','ratings_4','small_image_url']
    book_dropped_rated = book_with_totalRatingCount.drop(columns, axis=1)


    popularity_threshold = 100
    rating_popular_book = book_dropped_rated.query('totalRatingCount >= @popularity_threshold')


    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    book_cleaned = rating_popular_book.drop_duplicates(['user_id', 'title'])
    book_cleaned_pivot = book_cleaned.pivot(index = 'title', columns = 'user_id', values = 'rating').fillna(0)
    book_cleaned_matrix = csr_matrix(book_cleaned_pivot.values)
    model_knn.fit(book_cleaned_matrix)

    recommended_books=[]

    
    book_name=get_book_info(name.str.lower(),book_cleaned_pivot)

    book_info=book_cleaned_pivot.query('title == [@book_name]').iloc[:].values.reshape(1,-1)
    distances, indices = model_knn.kneighbors(book_info, n_neighbors = 6)
    for i in range(0, len(distances.flatten())):
        if i != 0:
            recommended_books.append(book_cleaned_pivot.index[indices.flatten()[i]])
            print('{0}: {1}, with distance of {2}:'.format(i, book_cleaned_pivot.index[indices.flatten()[i]], distances.flatten()[i]))

    return recommended_books  
        