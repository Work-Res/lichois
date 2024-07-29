
import factory
from factory.django import DjangoModelFactory

from app_checklist.models import Region
from authentication.models import User
from citizenship.models import Board, Role, BoardMember


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

    name = factory.Faker('company')
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
