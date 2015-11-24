import pytest
from autoconstruccion import create_app, db
from sqlalchemy.exc import OperationalError


# define app fixture for pytest-flask
@pytest.fixture()
def app(request):
    # for now we test over sqlite in memory, so no empty db needed
    test_app = create_app('TESTING_MEMORY')
    db.init_app(test_app)
    with test_app.test_request_context():
        # test that the database on we are testing it's ended with '_test'
        # to avoid data corruption and/or deletion
        db_uri = test_app.config['SQLALCHEMY_DATABASE_URI']
        if not db_uri.endswith('_test'):
            pytest.skip(msg="Testing over a none '_test' database. Skipping")
        try:
            # Start the database clean.
            db.drop_all()
            db.create_all()
        except OperationalError:
            pytest.fail(msg="The tables can't be created. Maybe the db don't exists or it didn't have access")

    def teardown():
        with test_app.test_request_context():
            db.drop_all()
    request.addfinalizer(teardown)

    return test_app