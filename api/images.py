from . import *

import hashlib
import os
from io import BytesIO

from flask import request, abort, send_from_directory
from PIL import Image

from db import Images


@rest.route('upload', methods=['POST'])
def upload_image():
    abort(500, 'Not allowed')
    """
    上传文件
    :return:
    """
    file = request.files['file']
    if file is None:
        abort(400, 'No file part')
    # 尝试用Pillow打开文件
    # 需要一个BytesIO对象，用于存储文件的二进制数据
    try:
        img = Image.open(BytesIO(file.read()))
        # 获取图片的宽高
        width, height = img.size
        if max(width, height) > 2160:
            # 按照长边缩放
            scale = 2160 / max(width, height)
            new_width, new_height = int(width * scale), int(height * scale)
            # 使用ANTIALIAS滤波器，保持图片质量
            img = img.resize((new_width, new_height))
    except Exception as e:
        logger.info(f'Upload API: Failed to open image: {e}')
        abort(403, 'Failed to open image')
    # 计算图片的MD5值
    b_img: bytes = img.tobytes()
    img_md5: str = hashlib.md5(b_img).hexdigest()
    # 保存图片
    img_filename = img_md5 + '.jpg'
    img.save(os.path.join(img_path, img_filename), 'JPEG')
    return {'code': 200, 'path': img_filename}


@rest.route('list/all', methods=['GET'])
def list_all_images():
    # 解析请求参数
    page = request.args.get('page', default=1, type=int)
    per_page = min(request.args.get('per_page', default=10, type=int), 100)
    resources = Images.list_emojis_all(limit=per_page, offset=(page - 1) * per_page)
    if not resources:
        abort(404, 'No images found')
    result = []
    for item in resources:
        result.append({
            'image_url': f'/image/{item.get("image_id")}',
            'character': item.get('i_character'),
            'emotion': item.get('emotion'),
            'is_official': item.get('is_official')
        })
    return result


@rest.route('list/custom', methods=['GET'])
def search_character():
    # 解析请求参数
    character = request.args.get('character', default=None, type=str)
    if character is None:
        abort(400, 'No character specified')
    page = request.args.get('page', default=1, type=int)
    per_page = min(request.args.get('per_page', default=10, type=int), 100)
    resources = Images.list_emojis_by_character(i_character=character, limit=per_page, offset=(page - 1) * per_page)
    if not resources:
        abort(404, 'No images found')
    result = []
    for item in resources:
        result.append({
            'image_url': f'/image/{item.get("image_id")}',
            'emotion': item.get('emotion'),
            'is_official': item.get('is_official')
        })


@app.route('/image/<path:image_id>', methods=['GET'])
def get_image(image_id):
    # 从数据库中获取图片的路径
    image_path = Images.get_image_path_by_id(image_id=image_id)
    print(os.path.join(img_path, image_path))
    return send_from_directory(img_path, image_path)
