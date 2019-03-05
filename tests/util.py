from http import HTTPStatus


def assert_response(res, status_code):
    assert res.headers.get('Content-Type') == 'application/json'
    assert res.status_code == status_code


def get_all_pages(client, path, rows_key, status_code=HTTPStatus.OK, query_params=None):
    all_rows = []
    if query_params is None:
        query_params = {}
    query_params['limit'] = 2

    res = client.get(path=path, query_string=query_params)
    assert_response(res, status_code)
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
        assert_response(res, status_code)
        data = res.json
        rows = data[rows_key]
        next_mark = data['pagination']['next_mark']

    return all_rows
