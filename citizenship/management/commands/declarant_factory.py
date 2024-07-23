import factory

from faker import Faker
from datetime import date

from app_oath.models import Declarant

fake = Faker()


class DeclarantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Declarant

    citizen_of_botswana = True
    citizen_of_country = 'Yes'
    country_of_birth = 'Botswana'
    place_of_birth = factory.LazyAttribute(lambda x: fake.city())
    date_of_birth = factory.LazyFunction(lambda: date(1990, 10, 10))
    full_age = True
    married_person = False
    not_ordinary_resident = False
    particulars_true = True
    renounce_citizenship = True
