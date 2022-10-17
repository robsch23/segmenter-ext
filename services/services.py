import ast
import os.path
from io import BytesIO
import requests
from pdf2image import convert_from_bytes
from loko_extensions.business.decorators import extract_value_args
from sanic import response
from sanic import Sanic, Blueprint
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc
from business.searchBox_core import searchBox_page
from business.segment_core import segmentation_page
from config.app_config import SERVICES_PORT, BASE_URL, DIR_SEGMENT, DIR_SEARCHBOX
from utils.logger_utils import stream_logger
from utils.ppom_utils import get_version

app = Sanic('segmenter_app')
swagger_blueprint.url_prefix = "/api"
app.blueprint(swagger_blueprint)
bp = Blueprint("default", url_prefix='loko/segmenter/')
app.config["API_TITLE"] = 'Segmenter LoKo'
app.config["API_VERSION"] = get_version()
app.config.API_DESCRIPTION = "Segmenter LoKo Swagger"
app.static('/web', "/frontend/dist")
CORS(app)

logger = stream_logger(__name__)


# home
@app.route('/web')
async def index(request):
    return await response.file('/frontend/dist/index.html')


@app.route('/images/<path:path>')
@doc.consumes(doc.String(name='path'), location='path')
async def get_images(request, path):
    url = os.path.join(BASE_URL, path)
    resp = requests.get(url)
    if resp.raise_for_status():
        return response.json('Images paths not found')

    return response.raw(resp.content)


@app.route('/load_segment')
async def load_segment(request):
    url = os.path.join(BASE_URL, DIR_SEGMENT)
    url_local = '/images/'
    resp = requests.get(url)
    if resp.raise_for_status():
        return response.json('Images paths not found')

    items = resp.json().get('items')
    items.reverse()

    list_response = []
    for item in items:
        url_img = url_local + item.get('path')
        list_response.append({'image': url_img})

    return response.json(list_response)


@app.route('/delete_segment', methods=['DELETE'])
async def delete_segment(request):
    url = os.path.join(BASE_URL, DIR_SEGMENT)
    requests.delete(url)

    return response.json('Images successfully deleted')


@app.route('/load_searchBox')
async def load_searchbox(request):
    url = os.path.join(BASE_URL, DIR_SEARCHBOX)
    url_local = '/images/'
    resp = requests.get(url)
    if resp.raise_for_status():
        return response.json('Images paths not found')

    items = resp.json().get('items')
    items.reverse()

    list_response = []
    for item in items:
        url_img = url_local + item.get('path')
        list_response.append({'image': url_img})

    return response.json(list_response)


@app.route('/delete_searchBox', methods=['DELETE'])
async def delete_searchbox(request):
    url = os.path.join(BASE_URL, DIR_SEARCHBOX)
    requests.delete(url)

    return response.json('Images successfully deleted')


# segment
@bp.post('/segment')
@doc.summary('Segmentation of doc')
@doc.tag('Segmenter')
@extract_value_args(file=True)
async def segmenter(file, args):
    # get params
    dpi = args.get('dpi')
    save_imgs = args.get('save_images')
    width_kernel, height_kernel = str(args.get('range_kernel_size')).split(',')[0], \
                                  str(args.get('range_kernel_size')).split(',')[1]
    dilate_iteration = int(args.get('dilate_iteration'))
    min_box_height, max_box_height = str(args.get('range_blocks_height')).split(',')[0], \
                                     str(args.get('range_blocks_height')).split(',')[1]
    min_box_width, max_box_width = str(args.get('range_blocks_width')).split(',')[0], \
                                   str(args.get('range_blocks_width')).split(',')[1]
    min_box_area, max_box_area = str(args.get('range_blocks_area')).split(',')[0], \
                                 str(args.get('range_blocks_area')).split(',')[1]

    # start convert
    pages = convert_from_bytes(file[0].body, dpi=dpi, fmt='pdf')
    dict_response = {}
    for i, page in enumerate(pages):
        list_box_page = segmentation_page(page,
                                          dilation_kernel_size=(int(width_kernel), int(height_kernel)),
                                          dilate_iteration=dilate_iteration,
                                          range_box_height=(int(min_box_height), int(max_box_height)),
                                          range_box_width=(int(min_box_width), int(max_box_width)),
                                          range_box_area=(int(min_box_area), int(max_box_area))
                                          )
        dict_response.update({f'page_{str(i)}': list_box_page})

    # save file in data loko
    if save_imgs:
        url = os.path.join(BASE_URL, DIR_SEGMENT)
        for key in dict_response.keys():
            for i, string_bytes in enumerate(dict_response[key]):
                file = BytesIO(ast.literal_eval(string_bytes))
                file.name = f'block_{str(key)}_n_{str(i)}.png'
                file.seek(0)
                requests.post(url, files={"file": file})

    return response.json(dict_response)


# search box
@bp.post('/search_box')
@doc.summary('Search box, checkbox and outlined elements in the document')
@doc.tag('Search Box')
@extract_value_args(file=True)
async def search_box(file, args):
    # get params
    dpi = args.get('dpi')
    save_imgs = args.get('save_images')
    min_box_height, max_box_height = str(args.get('range_box_height')).split(',')[0], \
                                     str(args.get('range_box_height')).split(',')[1]
    min_box_width, max_box_width = str(args.get('range_box_width')).split(',')[0], \
                                   str(args.get('range_box_width')).split(',')[1]
    min_box_area, max_box_area = str(args.get('range_box_area')).split(',')[0], \
                                 str(args.get('range_box_area')).split(',')[1]

    pages = convert_from_bytes(file[0].body, dpi=dpi, fmt='pdf')
    dict_response = {}
    for i, page in enumerate(pages):
        list_box_page = searchBox_page(page,
                                       range_box_height=(int(min_box_height), int(max_box_height)),
                                       range_box_width=(int(min_box_width), int(max_box_width)),
                                       range_box_area=(int(min_box_area), int(max_box_area))
                                       )
        dict_response.update({f'page_{str(i)}': list_box_page})

    # save file in data loko
    if save_imgs:
        url = os.path.join(BASE_URL, DIR_SEARCHBOX)
        for key in dict_response.keys():
            for i, string_bytes in enumerate(dict_response[key]):
                file = BytesIO(ast.literal_eval(string_bytes))
                file.name = f'box_{str(key)}_n_{str(i)}.png'
                file.seek(0)
                requests.post(url, files={"file": file})

    return response.json(dict_response)


app.blueprint(bp)
app.run("0.0.0.0", port=SERVICES_PORT, auto_reload=False, debug=False, access_log=False)
