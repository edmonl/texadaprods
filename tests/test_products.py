from http import HTTPStatus

from util import assert_response, get_all_pages


def test_create(client):
    prod = {'description': 'test product'}
    res = client.post('/products', json=prod)
    assert_response(res, HTTPStatus.CREATED)
    res_prod = res.json
    id = res_prod.get('id')
    assert 'id' is not None
    assert res.headers.get('Location') == 'http://localhost/products/{}'.format(id)
    expected = prod.copy()
    expected['id'] = id
    assert res_prod == expected

    assert_response(client.post('/products'), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/products', json={}), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/products', json={'description': ''}), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/products', json={'description': 1}), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/products', data=prod, content_type='text/plain'), HTTPStatus.BAD_REQUEST)


def test_list(client):
    prods = get_all_pages(client, '/products', 'products')
    assert sorted(prods, key=lambda p: p['id']) == [
        {'id': 1, 'description': 'Cesna 120'},
        {'id': 2, 'description': 'DC-6 Twin Otter'},
        {'id': 3, 'description': 'Piper M600'},
        {'id': 4, 'description': 'Art Boom 6500'},
    ]


def test_get(client):
    res = client.get('/products/1')
    assert_response(res, HTTPStatus.OK)
    assert res.json == {'id': 1, 'description': 'Cesna 120'}

    assert_response(client.get('/products/9'), HTTPStatus.NOT_FOUND)


def test_update(client):
    assert_response(client.put('/products/1', json={'id': 1, 'description': 'modified'}), HTTPStatus.NO_CONTENT)
    res = client.get('/products/1')
    assert_response(res, HTTPStatus.OK)
    assert res.json == {'id': 1, 'description': 'modified'}

    assert_response(client.put('/products/1', json={'description': 'modified'}), HTTPStatus.NO_CONTENT)
    assert_response(client.put('/products/2', json={'id': 1, 'description': 'modified'}), HTTPStatus.BAD_REQUEST)
    assert_response(client.put('/products/9', json={'id': 9, 'description': 'modified'}), HTTPStatus.NOT_FOUND)
    assert_response(client.put('/products/9', json={}), HTTPStatus.BAD_REQUEST)
    assert_response(client.put('/products/9', json={'id': 'invalid', 'description': 'modified'}), HTTPStatus.BAD_REQUEST)


def test_delete(client):
    assert_response(client.delete('/products/1'), HTTPStatus.NO_CONTENT)
    assert_response(client.delete('/products/1'), HTTPStatus.NOT_FOUND)
    assert_response(client.delete('/products/9x'), HTTPStatus.NOT_FOUND)
