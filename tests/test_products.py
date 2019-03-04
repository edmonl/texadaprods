from http import HTTPStatus

def _assert_response(res, status_code):
    assert res.headers.get('Content-Type') == 'application/json'
    assert res.status_code == status_code


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
