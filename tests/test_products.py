from http import HTTPStatus

def _assert_response(res, status_code):
    assert res.headers.get('Content-Type') == 'application/json'
    assert res.status_code == status_code


def _test_pagination(client, path, rows_key, status_code=HTTPStatus.OK, query_params=None):
    all_rows = []
    if query_params is None:
        query_params = {}
    query_params['limit'] = 2

    res = client.get(path=path, query_string=query_params)
    _assert_response(res, status_code)
    data = res.json
    rows = data[rows_key]
    next_mark = data['pagination']['next_mark']
    while len(rows) > 0:
        assert len(rows) <= 2
        all_rows.extend(rows)
        if len(rows) < 2:
            break
        query_params['mark'] = next_mark
        res = client.get(path=path, query_string=query_params)
        _assert_response(res, status_code)
        data = res.json
        rows = data[rows_key]
        next_mark = data['pagination']['next_mark']

    return all_rows


def test_create(client):
    prod = {'description': 'test product'}
    res = client.post('/products', json=prod)
    _assert_response(res, HTTPStatus.CREATED)
    res_prod = res.json
    id = res_prod.pop('id', None)
    assert 'id' is not None
    assert res.headers.get('Location') == 'http://localhost/products/{}'.format(id)
    assert res_prod == prod

    _assert_response(client.post('/products'), HTTPStatus.BAD_REQUEST)
    _assert_response(client.post('/products', json={}), HTTPStatus.BAD_REQUEST)


def test_list(client):
    prods = _test_pagination(client, '/products', 'products')
    assert sorted(prods, key=lambda p: p['id']) == [
        {'id': 1, 'description': 'Cesna 120'},
        {'id': 2, 'description': 'DC-6 Twin Otter'},
        {'id': 3, 'description': 'Piper M600'},
        {'id': 4, 'description': 'Art Boom 6500'},
    ]


def test_get(client):
    res = client.get('/products/1')
    _assert_response(res, HTTPStatus.OK)
    assert res.json == {'id': 1, 'description': 'Cesna 120'}

    _assert_response(client.get('/products/9'), HTTPStatus.NOT_FOUND)


def test_put(client):
    _assert_response(client.put('/products/1', json={'id': 1, 'description': 'modifed'}), HTTPStatus.NO_CONTENT)
    _assert_response(client.put('/products/1', json={'description': 'modifed'}), HTTPStatus.NO_CONTENT)
    _assert_response(client.put('/products/2', json={'id': 1, 'description': 'modifed'}), HTTPStatus.BAD_REQUEST)
    _assert_response(client.put('/products/9', json={'id': 9, 'description': 'modifed'}), HTTPStatus.NOT_FOUND)


def test_delete(client):
    _assert_response(client.delete('/products/1'), HTTPStatus.NO_CONTENT)
    _assert_response(client.delete('/products/9'), HTTPStatus.NOT_FOUND)


def test_list_locations(client):
    locs = _test_pagination(client, '/products/1/locations', 'locations')

    def remove_id(loc):
        loc.pop('id')
        return loc

    assert sorted(map(remove_id, locs), key=lambda l: l['datetime']) == [
      {'product_id': 1, 'datetime': '2016-10-12 17:00:00', 'longitude': 43.2583264, 'latitude': -81.8149807, 'elevation': 500},
      {'product_id': 1, 'datetime': '2016-10-13 17:00:00', 'longitude': 42.559112, 'latitude': -79.286693, 'elevation': 550},
      {'product_id': 1, 'datetime': '2016-10-14 17:00:00', 'longitude': 43.559112, 'latitude': -85.286693, 'elevation': 600},
      {'product_id': 1, 'datetime': '2016-10-15 17:00:00', 'longitude': 42.3119735, 'latitude': -83.0941179, 'elevation': 650},
    ]
