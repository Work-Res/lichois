import factory

from faker import Faker
from factory.django import DjangoModelFactory

from app_checklist.models import Region
from authentication.models import User
from citizenship.models import Board, Role, BoardMember
from faker.providers import BaseProvider

fake = Faker()


class BotswanaCityProvider(BaseProvider):

    cities = [
        'Gaborone Board', 'Francistown Board', 'Molepolole Board', 'Serowe Board', 'Maun Board',
        'Mochudi Board', 'Kanye Board', 'Palapye Board', 'Selibe Phikwe Board', 'Lobatse Board',
        'Ramotswa Board', 'Thamaga Board', 'Letlhakane Board', 'Mahalapye Board', 'Tlokweng Board'
    ]

    def botswana_city(self):
        return self.random_element(self.cities)

fake.add_provider(BotswanaCityProvider)


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    name = factory.Faker('city')
    code = factory.Faker('postcode')
    description = factory.Faker('text')
    valid_from = factory.Faker('date_this_decade')
    valid_to = factory.Faker('date_this_century')
    active = factory.Faker('boolean')


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Faker('job')


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.LazyAttribute(lambda x: fake.botswana_city())
    region = factory.SubFactory(RegionFactory)
    description = factory.Faker('text')

    @factory.post_generation
    def quorum_roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.quorum_roles.add(role)
        else:
            # Default to creating and adding 2 roles
            self.quorum_roles.add(RoleFactory(), RoleFactory())


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class BoardMemberFactory(DjangoModelFactory):
    class Meta:
        model = BoardMember

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    role = factory.SubFactory(RoleFactory)
