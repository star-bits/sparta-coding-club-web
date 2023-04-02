# 웹개발 종합반

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

### 1. app.py

```python
@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({},{'_id':False}))

    return jsonify({'result': all_comments})
```

### 2. index.html

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
