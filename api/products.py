from http import HTTPStatus
from textwrap import dedent

from flask import abort, Blueprint, jsonify, request, url_for

from . import db

blueprint = Blueprint('products', __name__)


def _get_prod_json():
    product = request.get_json()
    if product is None or 'description' not in product:
        abort(HTTPStatus.BAD_REQUEST)
    return product


def _get_page_args():
    mark = request.args.get('mark', default=0, type=int)
    limit = request.args.get('limit', default=1000, type=int)
    if limit < 0 or limit > 10000:
        abort(HTTPStatus.BAD_REQUEST)
    return mark, limit


def _page(rows_key, execute_cursor):
    mark, limit = _get_page_args()
    if limit <= 0:
        return jsonify({'pagination': {'next_mark': mark}, rows_key: []})
    with db.cursor() as cur:
        execute_cursor(cur, mark, limit)
        cur.arraysize = limit
        rows = cur.fetchall()
    return jsonify({
        rows_key: rows,
        'pagination': {'next_mark': max((r['id'] for r in rows), default=mark)}
    })


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


@blueprint.route('', methods=['GET'])
def list():
    def execute_cursor(cur, mark, limit):
        cur.execute('SELECT * FROM product WHERE id > ? ORDER BY id ASC LIMIT ?', (mark, limit))

    return _page('products', execute_cursor)


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
    loc = request.get_json()
    if product is None or 'description' not in product:
        abort(HTTPStatus.BAD_REQUEST)
    return loc


@blueprint.route('/<int:prod_id>/locations', methods=['GET'])
def list_locations(prod_id):
    def execute_cursor(cur, mark, limit):
        cur.execute('SELECT * FROM location WHERE product_id = ? AND id > ? ORDER BY id ASC LIMIT ?',
                    (prod_id, mark, limit))

    return _page('locations', execute_cursor)


@blueprint.route('/<int:prod_id>/locations', methods=['PUT'])
def set_locations(prod_id):
    locs = request.get_json()
    if not locs:
        abort(HTTPStatus.BAD_REQUEST)


    mark = request.args.get('mark', type=int)
    next_mark = request.args.get('next_mark', type=int)
    if mark is None or next_mark is None:
        abort(HTTPStatus.BAD_REQUEST)
    if mark > next_mark:
        mark, next_mark = next_mark, mark

    with db.cursor() as cur:
        cur.execute('DELETE FROM location WHERE id > ? AND id <= ?', (mark, next_mark))
        cur.executemany(
            dedent('''\
                INSERT INTO location (id, datetime, latitude, longitude, elevation)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT REPLACE'''),
            ((l['id'], l['datetime'], l['latitude'], l['longitude'], l['elevation']) for l in locs))

    return '', HTTPStatus.NO_CONTENT
