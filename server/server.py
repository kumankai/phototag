from flask import Flask, request, send_file
import src.controller.dbactions as db
import src.api.imagge as im
import src.helper.helper as h
import os, uuid

app = Flask(__name__)
imgsdir = f"{os.getcwd()}/server/src/resources/uploads"


# POST /api/image
@app.route("/api/image", methods=["POST"])
def image():
    if "file" not in request.files:
        return {"err": "File not included"}, 400

    # Save locally with unique name
    file = request.files["file"]
    filename = str(uuid.uuid4()) + ".jpg"
    file.save(f"{imgsdir}/{filename}")

    # Call api to get list of tags
    with open(f"{imgsdir}/{filename}", "rb") as f:
        tags = im.get_tags(f)

    # Save file to database here
    db.saveimage(filename, tags)

    return {"message": "File saved"}, 201


# GET /api/tags?from=<from_date>&to=<to_date>
@app.route("/api/tags")
def getTags():
    from_date = h.parse_datetime(request.args.get("from"))
    to_date = h.parse_datetime(request.args.get("to"))
    tags = db.getTags(from_date, to_date)

    res = {
        "from": from_date,
        "to": to_date,
        "tag": tags,
    }

    return res, 200


# GET /personDetected?from=<from_date>&to=<to_date>
@app.route("/api/personDetected")
def personDetected():
    from_date = h.parse_datetime(request.args.get("from"))
    to_date = h.parse_datetime(request.args.get("to"))
    presence = db.detectppl(from_date, to_date)

    res = {
        "from": from_date,
        "to": to_date,
        "personDetected": presence,
    }

    return res, 200


# GET /api/popularTags
@app.route("/api/popularTags")
def popularTags():
    topfive = db.getpopular()
    res = []

    for tag in topfive:
        obj = {"tag": tag[0], "count": str(tag[1])}
        res.append(obj)

    return res, 200


# GET /api/image/<filename>
@app.route("/api/image/<filename>")
def getimage(filename):
    file = f"{imgsdir}/{filename}.jpg"
    return send_file(file)


if __name__ == "__main__":
    db.createtable()
    app.run(host="10.16.49.115", port=9000, debug="True")
