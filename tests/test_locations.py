from http import HTTPStatus

from util import assert_response, get_all_pages


def test_create(client):
    loc = {
        'product_id': 1,
        'datetime': '2010-10-10T08:00:00-04:00',
        'longitude': 33,
        'latitude': -33,
        'elevation': 33,
    }
    res = client.post('/locations', json=loc)
    assert_response(res, HTTPStatus.CREATED)
    res_loc = res.json
    id = res_loc.get('id')
    assert 'id' is not None
    assert res.headers.get('Location') == 'http://localhost/locations/{}'.format(id)
    expected = res_loc.copy()
    expected['id'] = id
    assert res_loc == expected

    assert_response(client.post('/locations'), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/locations', json={}), HTTPStatus.BAD_REQUEST)
    assert_response(client.post('/locations', data=loc, content_type='text/plain'), HTTPStatus.BAD_REQUEST)

    bad_loc = loc.copy()
    bad_loc['product_id'] = 10
    assert_response(client.post('/locations', json=bad_loc), HTTPStatus.CONFLICT)

    bad_loc = loc.copy()
    bad_loc['longitude'] = 190
    assert_response(client.post('/locations', json=bad_loc), HTTPStatus.BAD_REQUEST)

    bad_loc = loc.copy()
    bad_loc['datetime'] = 'notadatetime'
    assert_response(client.post('/products', json=bad_loc), HTTPStatus.BAD_REQUEST)


def test_get(client):
    res = client.get('/locations/1')
    assert_response(res, HTTPStatus.OK)
    assert res.json == {
        'id': 1,
        'product_id': 1,
        'datetime': '2016-10-12 17:00:00',
        'longitude': 43.2583264,
        'latitude': -81.8149807,
        'elevation': 500,
    }

    assert_response(client.get('/locations/x'), HTTPStatus.NOT_FOUND)
    assert_response(client.get('/locations/99999'), HTTPStatus.NOT_FOUND)


def test_list(client):
    locs = get_all_pages(client, '/locations', 'locations', query_params={'product_id': 1})
    assert sorted(locs, key=lambda l: l['id']) == [
        {'id': 1, 'product_id': 1, 'datetime': '2016-10-12 17:00:00', 'longitude': 43.2583264, 'latitude': -81.8149807, 'elevation': 500},
        {'id': 2, 'product_id': 1, 'datetime': '2016-10-13 17:00:00', 'longitude': 42.559112, 'latitude': -79.286693, 'elevation': 550},
        {'id': 3, 'product_id': 1, 'datetime': '2016-10-14 17:00:00', 'longitude': 43.559112, 'latitude': -85.286693, 'elevation': 600},
        {'id': 4, 'product_id': 1, 'datetime': '2016-10-15 17:00:00', 'longitude': 42.3119735, 'latitude': -83.0941179, 'elevation': 650},
    ]

    assert_response(client.get('/locations'), HTTPStatus.BAD_REQUEST)

    locs = get_all_pages(client, '/locations', 'locations', query_params={
        'product_id': 1,
        'from': '2016-10-12 12:00:00-05:00',
    })
    assert len(locs) == 1
    assert locs[0] == {'id': 1, 'product_id': 1, 'datetime': '2016-10-12 17:00:00', 'longitude': 43.2583264, 'latitude': -81.8149807, 'elevation': 500}

    locs = get_all_pages(client, '/locations', 'locations', query_params={
        'product_id': 1,
        'to': '2016-10-12 12:00:00-05:00',
        'from': '2016-10-13 12:00:00-05:00',
    })
    assert len(locs) == 1
    assert locs[0] == {'id': 1, 'product_id': 1, 'datetime': '2016-10-12 17:00:00', 'longitude': 43.2583264, 'latitude': -81.8149807, 'elevation': 500}


def test_update(client):
    loc = {'datetime': '2018-10-15 17:00:00', 'longitude': 4, 'latitude': -8, 'elevation': 6}
    assert_response(client.put('/locations/1', json=loc), HTTPStatus.NO_CONTENT)
    loc['id'] = 1
    loc['product_id'] = 1
    res = client.get('/locations/1')
    assert_response(res, HTTPStatus.OK)
    assert res.json == loc

    assert_response(client.put('/locations/1', json={}), HTTPStatus.BAD_REQUEST)
    assert_response(client.put('/locations/2', json=loc), HTTPStatus.BAD_REQUEST)
    del loc['id']
    assert_response(client.put('/locations/1', json=loc), HTTPStatus.NO_CONTENT)
    assert_response(client.put('/locations/9999', json=loc), HTTPStatus.NOT_FOUND)


def test_delete(client):
    assert_response(client.delete('/locations/1'), HTTPStatus.NO_CONTENT)
    assert_response(client.delete('/locations/1'), HTTPStatus.NOT_FOUND)
    assert_response(client.delete('/locations/9x'), HTTPStatus.NOT_FOUND)
