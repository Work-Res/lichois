import factory
from faker import Faker

from datetime import datetime

from app_oath.models import OathDocument
from authentication.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: fake.user_name())
    email = factory.LazyAttribute(lambda x: fake.email())


class OathDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OathDocument

    user = factory.SubFactory(UserFactory)
    content = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=200))
    created_at = factory.LazyFunction(datetime.now)
    signed = factory.LazyAttribute(lambda x: fake.boolean())
    signed_at = factory.Maybe(
        'signed',
        yes_declaration=factory.LazyFunction(datetime.now),
        no_declaration=None
    )

