from flask import Flask, make_response, request
app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route("/")
def index():
    return "hello world"

@app.route("/no_content")
def no_content():
    return ("no content found", 204)

@app.route("/exp")
def index_explicit():
    res = make_response({"message": "Hello World"})
    res.status_code = 200
    return res

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return { "message" : f"Data of length {len(data)} found"}
        else:
            return { "message": "data is empty"}, 500
    except NameError:
        return { "message" : "Data not found"}, 404

@app.route("/name_search")
def name_search():
    first_name = request.args.get("q")
    if not first_name:
        return ("Invalid input parameter", 422)
    for person in data:
        if first_name.lower() == person["first_name"].lower():
            return person
    return ("Person not found", 404)

@app.get("/count")
def count():
    try:
        return { "data count": f"length of data is {len(data)}"}, 200
    except NameError:
        return {"message": "data not defined"}, 404

@app.get("/person/<uuid:uuid>")
def find_by_uuid(uuid):
    if not uuid:
        return {"message" : "bad requesst", "status_code" : 400}
    for person in data:
        if person["id"] == str(uuid):
            return person
    return { "message": "person not found", "status_code": 404}

@app.delete("/person/<uuid:uuid>")
def delete_by_uuid(uuid):
    if not uuid:
        return {"message" : "bad requesst", "status_code" : 400}
    for person in data:
        if person["id"] == str(uuid):
            data.remove(person)
            return {"id": uuid}
    return { "message": "person not found", "status_code": 404}






@app.post("/person")
def add_by_uuid():
    """
        Host: localhost:5000
        User-Agent: curl/7.58.0
        Accept: */*
        Content-Type: application/json
        Content-Length: 340
    """
    # print(request.headers)
    # print(request.server) # ('127.0.0.1', 5000)
    # print(request.url) # http://localhost:5000/person
    # print(request.access_route) # ImmutableList(['127.0.0.1'])
    # print(request.is_secure) # False
    # print(request.is_json) # True
    # print(request.cookies) # ImmutableMultiDict([])
    """
        '{\n        "id": "4e1e61b4-8a27-11ed-a1eb-0242ac120002",\n        "first_name": "John",\n        "last_name": "Horne",\n        "graduation_year": 2001,\n        "address": "1 hill drive",\n        "city": "Atlanta",\n        "zip": "30339",\n        "country": "United States",\n        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff"\n}'"""
    # print(request.get_data())
    """
        {
        'id': '4e1e61b4-8a27-11ed-a1eb-0242ac120002', 
        'first_name': 'John', 
        'last_name': 'Horne', 
        'graduation_year': 2001, 
        'address': '1 hill drive', 
        'city': 'Atlanta', 
        'zip': '30339', 
        'country': 'United States', 
        'avatar': 'http://dummyimage.com/139x100.png/cc0000/ffffff'
        }
    """ 
    # print(request.get_json())
    # new_person = request.get_json()
    # if not new_person:
    #     return { "message": "Invalid input params", "status": 422 }
    # data.append(new_person)
    # return { "message": new_person['id'], "status": 200}
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    # code to validate new_person ommited
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    return {"message": f"{new_person['id']}"}, 200

@app.errorhandler(404)
def api_not_found(error):
    return { "message": "API not found"}, 404