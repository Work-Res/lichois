from django.db import models


class EmployerModelMixin(models.Model):
    business_name = models.CharField(
        max_length=255,
        verbose_name='Full Business Name',
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Business Location/Address',

    )
    tel = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Telephone NO: ',
    )
    fax = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Fax NO: ',
    )
    type_of_service = models.CharField(
        max_length=255,
        verbose_name='Type of Goods and Services provided by the business',
    )
    job_title = models.CharField(
        max_length=255,
        verbose_name='Job Title',
    )
    job_description = models.TextField(
        verbose_name='Job Description',
    )
    renumeration = models.DecimalField(max_digits=10, decimal_places=2)

    period_permit_sought = models.IntegerField(
        verbose_name='Period which permit is sought',
    )

    has_vacancy_advertised = models.BooleanField(
        verbose_name='Has the vacancy been advertised? Yes/NO',
    )

    have_funished = models.BooleanField()

    reasons_funished = models.TextField(
        verbose_name='Have you furnished furnished the Commissioner of Labour with your manpower development, '
                     'training and localization program?'
                     'Yes/No. If no, please explain',

    )
    time_fully_trained = models.IntegerField(
        verbose_name='State the time required to have trainee fully-trained',
    )
    reasons_renewal_takeover = models.TextField(
        verbose_name='In case of renewal briefly and factually state reasons why trainee cannot take over',
    )
    reasons_recruitment = models.TextField(
        verbose_name='What are your main difficulties in securing local recruitment for this post?',
    )
    labour_enquires = models.TextField(
        verbose_name='Have you made recruitment enquiries with the employment services of Botswana on the availability of a suitable citizen for'
                     'the job you are offering to a non-citizen?',
    )
    no_bots_citizens = models.IntegerField(
        verbose_name='State number of locals or Botswana citizens in your establishment',
    )

    class Meta:
        app_label = "workresidentpermit"
        abstract = True
