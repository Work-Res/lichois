from pytest_factoryboy import register

from app.tests.factories import ApplicationVersionFactory, ApplicationStatusFactory

register(ApplicationStatusFactory)
register(ApplicationVersionFactory)

