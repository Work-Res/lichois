import factory

from datetime import date


from app.models import ApplicationStatus, ApplicationDocument, Application, ApplicationVersion, ApplicationUser


class ApplicationUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApplicationUser

    user_identifier = '317918'


class ApplicationDocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ApplicationDocument

    applicant = factory.SubFactory(ApplicationUserFactory)
    document_number = 'REF/RES/LAB-001'
    document_date = date.today()
    signed_date = date.today()
    submission_customer = 'test'


class ApplicationStatusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ApplicationStatus

    code = 'new'
    name = 'NEW'
    processes = 'WORK_RESIDENT_PERMIT,workpermit,visa'
    valid_from = date(2023, 1, 1)


class ApplicationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Application

    last_application_version_id = 1
    application_document = factory.SubFactory(ApplicationDocumentFactory)
    application_status = factory.SubFactory(ApplicationStatusFactory)


class ApplicationVersionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ApplicationVersion

    application = factory.SubFactory(ApplicationFactory)
    version_number = 1
    comment = "NA"
