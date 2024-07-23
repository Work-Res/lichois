import factory
from faker import Faker

from citizenship.models import KgosanaCertificate

fake = Faker()


class KgosanaCertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KgosanaCertificate

    kgosana_surname = factory.LazyAttribute(lambda x: fake.last_name())
    kgosana_firstname = factory.LazyAttribute(lambda x: fake.first_name())
    id_elder_firstname = factory.LazyAttribute(lambda x: fake.first_name())
    id_elder_lastname = factory.LazyAttribute(lambda x: fake.last_name())
    community = factory.LazyAttribute(lambda x: fake.city())
    settlement_year = factory.LazyAttribute(lambda x: fake.date_this_century())
    certificate_place = factory.LazyAttribute(lambda x: fake.address())
    certificate_datetime = factory.LazyAttribute(lambda x: fake.date_time_this_century())
    kgosana_sign = factory.LazyAttribute(lambda x: fake.word())
