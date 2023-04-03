# 웹개발 종합반

- GitHub Pages deployment: https://star-bits.github.io/sparta-coding-club-web-ex2/
- AWS deployment: 

## POST (저장하기)

### 1. index.html: body에서 입력받고 script에서 처리해서 fetch로 POST API 콜

`<textarea id="review">` -> `<button onclick="save_review()">` -> `$("#review").val()` -> `"review_give"` -> `formData`

```js
// 1. POST (저장하기)
function save_review() {
    let url = $("#url").val()
    let star = $('#star').val()
    let review = $("#review").val()

    let formData = new FormData();
    formData.append("url_give", url);
    formData.append("star_give", star);
    formData.append("review_give", review);

    fetch('/review_api', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        // fetch로 POST API 콜 하고 data를 넘겨받음
        console.log(data)
        alert(data["post_api_return"]);
        window.location.reload()
    });
}
```

### 2. app.py: 넘겨받은 데이터를 DB에 저장

`formData` -> `'review_give'` -> `review_receive` -> `doc` -> `db.insert_one(doc)`

```python
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
```

## GET (가져오기)

### 3. app.py: DB에서 가져와서 fetch로 넘겨줄 준비

`db.find()` -> `all_reviews` -> `'get_api_return'`

```python
# 3. GET (가져오기)
@app.route("/review_api", methods=["GET"])
def review_get():
    all_reviews = list(db.review_db.find({},{'_id':False}))
    print(all_reviews)
    return jsonify({'get_api_return': all_reviews})
```

### 4. index.html: fetch로 넘겨받아서 body에 붙여넣음

`'get_api_return'` -> `rows` -> `a['review']` -> `review` -> `${review}`

```js
// 4. GET (가져오기)
function show_review() {
    fetch('/review_api').then((res) => res.json()).then((data) => {
        alert('가져오기 완료! (GET 연결 완료!)')

        let rows = data['get_api_return']
        console.log(rows)
        $("#review-list").empty()
        rows.forEach((a) => {
            let url = a['url']
            let star = a['star']
            let star_repeat = '⭐'.repeat(star)
            let review = a['review']
            let title = a['title']
            let image = a['image']

            let temp_html = `<div class="card h-100">
                                <img src="${image}"
                                    class="card-img-top">
                                <div class="card-body">
                                    <h5 class="card-title">${title.slice(0, -7)}</h5>
                                    <p>${star_repeat}</p>
                                    <p class="mycomment">${review}</p>
                                </div>
                            </div>`

            $("#review-list").append(temp_html)
        })
    })
}
```

## venv

```shell
python -m venv xvnv
source xvnv/bin/activate
pip install flask pymongo dnspython
```

## AWS

```shell
mkdir deploy
cp app.py deploy/application.py
cp -r templates deploy/templates
pip freeze > deploy/requirements.txt
cd deploy
```

Changes to make in `application.py`:
```python
# app = Flask(__name__)
application = app = Flask(__name__)

# app.run('0.0.0.0', port=5001, debug=True)
app.run()
```

```shell
pip install awsebcli

eb init

Select a default region (default is 3): 10
(aws-access-id): <Access key>
(aws-secret-key): <Secret access key>
Enter Application Name (default is "deploy"): 
It appears you are using Python. Is this correct? (Y/n): Y
Select a platform branch. (default is 1): 
Do you want to set up SSH for your instances? (Y/n): Y
Type a keypair name. (Default is aws-eb): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 

eb create myweb
```
