import factory

from faker import Faker


from citizenship.models import KgosiCertificate

fake = Faker()


class KgosiCertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KgosiCertificate

    kgosi_surname = factory.LazyAttribute(lambda x: fake.last_name())
    kgosi_firstname = factory.LazyAttribute(lambda x: fake.first_name())
    village = factory.LazyAttribute(lambda x: fake.city())
    tribe = factory.LazyAttribute(lambda x: fake.word())
    known_year = factory.LazyAttribute(lambda x: fake.date_this_century())
    community = factory.LazyAttribute(lambda x: fake.word())
    living_circumstance = factory.LazyAttribute(lambda x: fake.sentence(nb_words=10))
