import sqlite3
from datetime import datetime
from http import HTTPStatus
from textwrap import dedent

from flask import abort, Blueprint, g, jsonify, request, url_for
from flask_expects_json import expects_json

from . import db, pagination

blueprint = Blueprint('locations', __name__)

location_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'product_id': {'type': 'integer'},
        'datetime': {'type': 'string'},
        'longitude': {'type': 'number', 'minimum': -180, 'maximum': 180},
        'latitude': {'type': 'number', 'minimum': -90, 'maximum': 90},
        'elevation': {'type': 'integer'}
    },
    'required': ['datetime', 'longitude', 'latitude', 'elevation'],
}

new_location_schema = location_schema.copy()
new_location_schema['required'] = location_schema['required'].copy()
new_location_schema['required'].append('product_id')


@blueprint.route('', methods=['POST'])
@expects_json(new_location_schema)
def create():
    loc = g.data
    with db.cursor() as cur:
        try:
            cur.execute(
                dedent('''\
                    INSERT INTO location (product_id, datetime, longitude, latitude, elevation)
                    VALUES (?, DATETIME(?), ?, ?, ?)'''
                ),
                (loc['product_id'], loc['datetime'], loc['longitude'], loc['latitude'], loc['elevation']),
            )
        except sqlite3.IntegrityError as e:
            if str(e) == 'FOREIGN KEY constraint failed':
                abort(HTTPStatus.CONFLICT)
            raise
        new_id = cur.lastrowid
    loc['id'] = new_id
    res = jsonify(loc)
    res.headers.set('Location', url_for('.get', id=new_id))
    res.status_code = HTTPStatus.CREATED
    return res


@blueprint.route('/<int:id>', methods=['GET'])
def get(id):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM location WHERE id = ?', (id,))
        row = cur.fetchone()
    if row is None:
        abort(HTTPStatus.NOT_FOUND)
    return jsonify(row)


@blueprint.route('', methods=['GET'])
def list():
    prod_id = request.args.get('product_id', type=int)
    if prod_id is None:
        abort(HTTPStatus.BAD_REQUEST)
    from_dt = request.args.get('from')
    to_dt = request.args.get('to')
    if from_dt is None and to_dt is not None:
        abort(HTTPStatus.BAD_REQUEST)
    try:
        if from_dt is not None:
            from_dt = datetime.fromisoformat(from_dt)
        if to_dt is not None:
            to_dt = datetime.fromisoformat(to_dt)
            if from_dt > to_dt:
                from_dt, to_dt = to_dt, from_dt
            to_dt = to_dt.isoformat(' ', 'seconds')
        if from_dt is not None:
            from_dt = from_dt.isoformat(' ', 'seconds')
    except (ValueError, TypeError):
        abort(HTTPStatus.BAD_REQUEST)
    query = 'SELECT * FROM location WHERE product_id = ? AND id > ? {} ORDER BY id ASC LIMIT ?'

    def execute_cursor(cur, mark, limit):
        if from_dt is None:
            dt_range = ''
            query_args = (prod_id, mark, limit)
        elif to_dt is None:
            dt_range = 'AND datetime = DATETIME(?)'
            query_args = (prod_id, mark, from_dt, limit)
        else:
            dt_range = 'AND datetime >= DATETIME(?) AND datetime < DATETIME(?)'
            query_args = (prod_id, mark, from_dt, to_dt, limit)
        cur.execute(query.format(dt_range), query_args)

    return pagination.execute('locations', execute_cursor)


@blueprint.route('/<int:id>', methods=['PUT'])
@expects_json(location_schema)
def update(id):
    loc = g.data
    if loc.get('id', id) != id:
        abort(HTTPStatus.BAD_REQUEST)
    with db.cursor() as cur:
        cur.execute(
            'UPDATE location SET (datetime, longitude, latitude, elevation) = (?, ?, ?, ?) WHERE id = ?',
            (loc['datetime'], loc['longitude'], loc['latitude'], loc['elevation'], id),
        )
        if cur.rowcount <= 0:
            abort(HTTPStatus.NOT_FOUND)
    return '', HTTPStatus.NO_CONTENT


@blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with db.cursor() as cur:
        cur.execute('DELETE FROM location WHERE id = ?', (id,))
        if cur.rowcount <= 0:
            abort(HTTPStatus.NOT_FOUND)
    return '', HTTPStatus.NO_CONTENT
