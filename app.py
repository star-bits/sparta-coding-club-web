from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
# application = app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.csrgvbd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup



@app.route('/')
def home():
   return render_template('index.html')


# 2. POST (저장하기)
@app.route("/review_api", methods=["POST"])
def review_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    review_receive = request.form['review_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'url': url_receive,
        'star': star_receive,
        'review': review_receive,
        'title': ogtitle,
        'image': ogimage
    }
    db.review_db.insert_one(doc)

    return jsonify({'post_api_return': '저장하기 완료! (POST 연결 완료!)'})

   
# 3. GET (가져오기)
@app.route("/review_api", methods=["GET"])
def review_get():
    all_reviews = list(db.review_db.find({},{'_id':False}))
    # print(all_reviews)
    return jsonify({'get_api_return': all_reviews})

   
if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
   # app.run()
