from http import HTTPStatus

from flask import abort, Blueprint, g, jsonify, request, url_for
from flask_expects_json import expects_json

from . import db, pagination

blueprint = Blueprint('products', __name__)

product_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'description': {'type': 'string', 'minLength': 1},
    },
    'required': ['description'],
}


@blueprint.route('', methods=['POST'])
@expects_json(product_schema)
def create():
    product = g.data
    with db.cursor() as cur:
        cur.execute('INSERT INTO product(description) VALUES (?)', (product['description'],))
        new_id = cur.lastrowid
    product['id'] = new_id
    res = jsonify(product)
    res.headers.set('Location', url_for('.get', id=new_id))
    res.status_code = HTTPStatus.CREATED
    return res


@blueprint.route('', methods=['GET'])
def list():
    def execute_cursor(cur, mark, limit):
        cur.execute('SELECT * FROM product WHERE id > ? ORDER BY id ASC LIMIT ?', (mark, limit))

    return pagination.execute('products', execute_cursor)


@blueprint.route('/<int:id>', methods=['GET'])
def get(id):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM product WHERE id = ?', (id,))
        row = cur.fetchone()
    if row is None:
        abort(HTTPStatus.NOT_FOUND)
    return jsonify(row)


@blueprint.route('/<int:id>', methods=['PUT'])
@expects_json(product_schema)
def update(id):
    product = g.data
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
