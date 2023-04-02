# 웹개발 종합반

aws deploy
formatting
mongodb howto
venv gitignore
Index on hithub 
Requirements.tzt
Add bs4, AWS to desc

## POST (저장하기)

### 1. index.html: body에서 입력받고 script에서 처리해서 fetch로 POST API 콜

`<textarea id="comment">` -> `<button onclick="save_comment()">` -> `comment = $("#comment").val()` -> `formData.append("comment_give", comment` -> `fetch(guestbook, POST, formData)`

```js
function save_comment() {

    let name = $("#name").val()
    let comment = $("#comment").val()

    let formData = new FormData();
    formData.append("name_give", name);
    formData.append("comment_give", comment);

    fetch('/guestbook', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        //console.log(data)
        alert(data["msg"]);
    });
}
```

### 2. app.py: 넘겨받은 데이터를 DB에 저장

`comment_give` -> `guestbook_post()` -> `comment_receive` -> `doc` -> `db.fan.insert_one(doc)`

```python
@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.fan.insert_one(doc)
    return jsonify({'msg': '저장 완료(POST 연결 완료!)'})
```

## GET (가져오기)

### 1. app.py: DB에서 가져와서 fetch로 넘겨줄 준비

```python
@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({},{'_id':False}))

    return jsonify({'result': all_comments})
```

### 2. index.html: fetch로 넘겨받아서 body에 붙여넣음

```js
function show_comment() {
    fetch('/guestbook').then((res) => res.json()).then((data) => {
        // alert(data["msg"])
        let rows = data['result']

        console.log(rows)
        $("#comment-list").empty()
        rows.forEach((a)=>{
            let name = a['name']
            let comment = a['comment']

            let temp_html = `<div class="card">
                                <div class="card-body">
                                    <blockquote class="blockquote mb-0">
                                        <p>${comment}</p>
                                        <footer class="blockquote-footer">${name}</footer>
                                    </blockquote>
                                </div>
                            </div>`
            $("#comment-list").append(temp_html)
        })
    })
}
```

## venv

```shell
python -m venv xvnv
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

Select a default region: 10
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
