from http import HTTPStatus

from flask import abort, jsonify, request

from . import db

DEFAULT_LIMIT = 1000
MAX_LIMIT = 10000

def _get_page_args():
    mark = request.args.get('mark', default=0, type=int)
    limit = request.args.get('limit', default=DEFAULT_LIMIT, type=int)
    if limit < 0 or limit > MAX_LIMIT:
        abort(HTTPStatus.BAD_REQUEST)
    return mark, limit


def execute(rows_key, execute_cursor):
    mark, limit = _get_page_args()
    if limit <= 0:
        return jsonify({'pagination': {'next_mark': mark}, rows_key: []})
    with db.cursor() as cur:
        cur.arraysize = limit
        execute_cursor(cur, mark, limit)
        rows = cur.fetchall()
    return jsonify({
        rows_key: rows,
        'pagination': {'next_mark': max((r['id'] for r in rows), default=mark)}
    })
