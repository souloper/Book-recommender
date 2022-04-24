from flask import Flask, render_template, url_for, request, jsonify, redirect, json
import requests
from urllib.request import urlopen
from recommender import recommend
app = Flask(__name__)



# endpoint = "https://www.googleapis.com/books/v1/volumes"
# query = "harry potter"

# params = {"q": query, "maxResults": 1}
# response = requests.get(endpoint, params=params).json()
# for book in response["items"]:
#     volume = book["volumeInfo"]
#     title = volume["title"]
#     author = volume["authors"]
#     published = volume["publishedDate"]

#     #isbn = volume["industryIdentifiers"]
#     #isbn_10 = volume["industryIdentifiers[0].type"]
#     imageLinks = volume["imageLinks"]
#     thumbnail = imageLinks["thumbnail"]
#     # description = volume["description"]
#     # print(f"{title} {author} ({published}) | {thumbnail} ")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ["GET","POST"])
def predict():

    s = request.form.get('bookSearch')
    name = s
    api = "https://www.googleapis.com/books/v1/volumes?q=title:"
    resp = urlopen(api + name)

    book_data = json.load(resp)
    #endpoint = "https://www.googleapis.com/books/v1/volumes"
    #query = search 
    #params = {"q": query, "maxResults": 3}
    #response = requests.get(endpoint, params=params).json()   
    volume_info = book_data["items"][0]["volumeInfo"]
    author = volume_info["authors"]
    prettify_author = author if len(author) > 1 else author[0]

    #for book in response["items"]:
        #volume = book["volumeInfo"]
    title = book_data["items"][0]["volumeInfo"]["title"]
        
    published = book_data["items"][0]["volumeInfo"]["publishedDate"]
    verify_published = published if (published) else print("NIL")
        #isbn = volume["industryIdentifiers"][1]["identifier"]  
    imageLinks = book_data["items"][1]["volumeInfo"]["imageLinks"]["thumbnail"]
    
        #desc = book["volumeInfo"]["description"]
        #info = book["searchInfo"]["textSnippet"]
            
    #         #r = str(requests.get(endpoint, params=params, verify=False).content)
    #         # r = (requests.get(endpoint, params=params))["items"]
    return render_template('predict.html', t=s)
        # else:
        #     return render_template('predict.html')

# @app.route('/predict', methods = ["GET","POST"])
# def predict():

#     search = request.form.get('bookSearch')
#     return render_template('test.html', s=search)
# @app.route('/predict/recom', methods = ["GET","POST"])
#     def ():
#     render_template("recom.html")   

    
if __name__ == '__main__':
    app.run(debug=True, threaded=True)

