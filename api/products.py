from http import HTTPStatus

from flask import abort, Blueprint, jsonify, request, url_for

from . import db

blueprint = Blueprint('products', __name__)


def _get_prod_json():
    product = request.get_json()
    if product is None or 'description' not in product:
        abort(HTTPStatus.BAD_REQUEST)
    return product


@blueprint.route('', methods=['POST'])
def create():
    product = _get_prod_json()
    with db.cursor() as cur:
        cur.execute('INSERT INTO product(description) VALUES (?)', (product['description'],))
        new_id = cur.lastrowid
    product['id'] = new_id
    res = jsonify(product)
    res.headers.set('Location', url_for('.get', id=new_id))
    res.status_code = HTTPStatus.CREATED
    return res


@blueprint.route('/<int:id>', methods=['GET'])
def get(id):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM product WHERE id = ?', (id,))
        row = cur.fetchone()
    if row is None:
        abort(HTTPStatus.NOT_FOUND)
    return jsonify(row)


@blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    product = _get_prod_json()
    if product.get('id', id) != id:
        abort(HTTPStatus.BAD_REQUEST)
    with db.cursor() as cur:
        cur.execute('UPDATE product SET description = ? WHERE id = ?', (product['description'], id))
        if cur.rowcount <= 0:
            abort(HTTPStatus.NOT_FOUND)
    return '', HTTPStatus.NO_CONTENT


@blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with db.cursor() as cur:
        cur.execute('DELETE FROM product WHERE id = ?', (id,))
        if cur.rowcount <= 0:
            abort(HTTPStatus.NOT_FOUND)
    return '', HTTPStatus.NO_CONTENT


def _get_loc_json():
    product = request.get_json()
    if product is None or 'description' not in product:
        abort(HTTPStatus.BAD_REQUEST)
    return product
