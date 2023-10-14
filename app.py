from flask import Flask

app = Flask(__name__)

store = [
    {
        "name": "My Store",
        "items": [
            {
                "name":"chair",
                "price":15.99
            }
        ]
    }   
]

@app.get('/store')
def get_stores():
    return {"store":store}