#v0.0.1 python_version = 3.3
#-*- coding:utf8 -*-
from flask import Flask
from flask import request
from flask_restful import reqparse,Api,Resource
import qrcode
from PIL import Image,ImageDraw,ImageFont


app = Flask(__name__)
api = Api(app)

ITEMS = {
    'item1': {'name': 'Allen', 'age': 19},
    'item2': {'name': 'Lily', 'age': 18},
    'item3': {'name': 'James', 'age': 20},
}

parser = reqparse.RequestParser()
parser.add_argument('name',type=str,help=('need name'))
parser.add_argument('age',type=int,help=('need age'))


def creat_qr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return img

def text2img(str,font_color="Blue",font_size=25):
    font = ImageFont.truetype('simsun.ttc',font_size)
    mark = Image.new('RGBA',(100,100))
    draw = ImageDraw.ImageDraw(mark,"RGBA")
    draw.setfont(font)
    draw.text((0,30),str,fill=font_color)
    return mark
    #text = str.split('\n')
    #mark_width = 0
    #for i in range(len(text)):
    #    (width, height) = font.getsize(text[i])
    #    if mark_width < width:
    #        mark_width = width
    #mark_height = height * len(text)

    #mark = Image.new('RGBA',(mark_width,mark_height))
    #draw = ImageDraw.ImageDraw(mark,"RGBA")
    #draw.setfont(font)
    #for i in range(len(text)):
    #    (width, height) = font.getsize(text[i])
    #    draw.text((0, i * height), text[i], fill=font_color)
    #return mark


#@app.route('/items/<item_id>')
class Todo(Resource):
    def put(self,item_id):
        args = parser.parse_args()
        item = {'name': args['name'], 'age': args['age']}
        ITEMS[item_id] = item
        return item,201
    def get(self,item_id):
        return ITEMS[item_id], 200

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api_v1/<name>' , methods=['GET','POST'])
def name_search(name):
    if request.method == 'POST':
        return 'POST %s' % name
    else :
        return 'GET %s' %name
    #return '%s' % name

api.add_resource( Todo, '/items/<item_id>')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
