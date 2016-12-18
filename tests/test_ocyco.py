# -*- coding: utf-8 -*-
"""
    Ocyco Tests

    Tests the Ocyco server application.

    :copyright: (c) 2016 by Raphael Lehmann.
    :license: AGPLv3, see LICENSE for more details.
"""

import pytest
from app import app as ocyco
from app import init_db

init_db()

@pytest.fixture
def client(request):
    client = ocyco.test_client()

    def teardown():
        # nothing?!
        pass
    request.addfinalizer(teardown)
    return client


def database_clear():
    with ocyco.app_context():
        ocyco.db.drop_all()
        ocyco.db.create_all()


def test_no_tracks(client):
    """Checks if no tracks exist in a blank database."""
    rv = client.get('/track/num')
    assert ':0' in rv.data


def test_add_track(client):
    """Add/upload a valid track."""
    database_clear()
    track_json = '{"data":[{"lat":10,"lon":5,"time":1582015058015},{"lat":11,"lon":4,"time":1582015068800},{"lat":12,"lon":3,"time":1582015078012},{"lat":13,"lon":4,"time":1582015088000},{"lat":13.500,"lon":5.25000,"time":1582015178005}],"public":true,"length":4.242424,"duration":1902}'
    rv = client.post('/track/add', data=track_json, content_type='application/json')
    assert 'created' in rv.data
    # TODO: read track_id from json and request track from api
    rv = client.get('/track/num')
    assert ':1' in rv.data
