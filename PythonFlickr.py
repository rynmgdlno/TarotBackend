from flask import Flask
from flask import request, jsonify
import requests
from io import BytesIO
from PIL import Image
import random

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=["GET"])
def tarot():
    api_key = '3ea4ad15f78cd2962c589daa3fec5f75'
    query = request.args.get('query')
    page = request.args.get('page')
    URL = f'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key={api_key}&tags={query}&page={page}&tag_mode=all&extras=url_s&per_page=20&format=json&nojsoncallback=1'

    # page_number = 1

    response = requests.get(URL).json()
    pages = response['photos']['pages']
    page = response['photos']['page']
    photos = response['photos']['photo']
    photo_urls = []

    for photo in photos:
        photo_urls.append(photo['url_s'])

    images = []
    image_palettes_all = []
    for image in photo_urls:
        # url = image["url"]
        img_response = requests.get(image)
        if img_response:
            try:
                img = Image.open(BytesIO(img_response.content))
                images.append(img)
            except IOError:
                continue

    for image in images:
        hex_palette = []
        image_palette = []
        width, height = image.size
        while len(hex_palette) < 5:
            try:
                rand_x = random.randint(1, width - 1)
                rand_y = random.randint(1, height - 1)
                color = img.getpixel((rand_x, rand_y))
                hex_color = f'{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                color_data = {
                    "id": len(hex_palette),
                    "hex": hex_color,
                    "red": color[0],
                    "green": color[1],
                    "blue": color[2]
                }
            except IndexError:
                continue
            if hex_color not in hex_palette:
                hex_palette.append(hex_color)
                image_palette.append(color_data)
        image_palettes_all.append(image_palette)
    # print(len(image_palettes_all))
    print(pages)
    print(jsonify(page, pages, image_palettes_all))
    return jsonify(page, pages, image_palettes_all)


app.run()
