import factory
from faker import Faker
from app_personal_details.models import DeceasedSpouseInfo, MarriageDissolutionInfo
from app_personal_details.models.name_change import NameChange
from citizenship.models import (
    LocalLanguageKnowledge,
    ResidencyPeriod,
    CriminalOffense,
    CountryOfResidence,
)

fake = Faker()


class DeceasedSpouseInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeceasedSpouseInfo

    country_of_death = factory.Faker("country")
    place_of_death = factory.Faker("city")
    date_of_death = factory.Faker("date")


class MarriageDissolutionInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MarriageDissolutionInfo

    country_of_dissolution = factory.Faker("country")
    place_of_dissolution = factory.Faker("city")
    date_of_dissolution = factory.Faker("date")


class NameChangeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NameChange

    previous_name = factory.Faker("name")
    new_name = factory.Faker("name")
    date_of_change = factory.Faker("date")


class LocalLanguageKnowledgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LocalLanguageKnowledge

    language_name = factory.Faker("word")
    proficiency_level = factory.Faker(
        "random_element", elements=["Basic", "Fluent", "Native"]
    )


class ResidencyPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResidencyPeriod

    period_from = factory.Faker("date")
    period_until = factory.Faker("date")
    country = factory.Faker("country")


class CriminalOffenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CriminalOffense

    offense_description = factory.Faker("sentence")
    date_of_conviction = factory.Faker("date")
    country_of_offense = factory.Faker("country")
    penalty_given = factory.Faker("sentence")


class CountryOfResidenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CountryOfResidence

    country = factory.Faker("country")
    period_from = factory.Faker("date")
    period_until = factory.Faker("date")


class FormLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "citizenship.FormL"  # You can use the app_label.model_name format

    deceased_spouse_info = factory.SubFactory(DeceasedSpouseInfoFactory)
    marriage_dissolution_info = factory.SubFactory(MarriageDissolutionInfoFactory)
    name_change = factory.SubFactory(NameChangeFactory)
    previous_application_date = factory.Faker("date")
    relation_description = factory.Faker("paragraph")
    citizenship_loss_circumstances = factory.Faker("paragraph")


    @factory.post_generation
    def residency_periods(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for period in extracted:
                self.residency_periods.add(period)
        else:
            self.residency_periods.add(ResidencyPeriodFactory())

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for language in extracted:
                self.languages.add(language)
        else:
            self.languages.add(LocalLanguageKnowledgeFactory())

    @factory.post_generation
    def criminal_offences(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for offense in extracted:
                self.criminal_offences.add(offense)
        else:
            self.criminal_offences.add(CriminalOffenseFactory())

    @factory.post_generation
    def countries_of_residence(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for country in extracted:
                self.countries_of_residence.add(country)
        else:
            self.countries_of_residence.add(CountryOfResidenceFactory())
