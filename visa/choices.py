from django.utils.translation import gettext_lazy as _

COMM_METHODS = (
    ('email', 'E-mail'),
    ('sms', 'SMS'),
    ('postal', 'Post')
)

ENTRY_FREQ = (
    ('single', 'Single'),
    ('multiple', 'Multiple')
)

PERIOD_MEASURE = (
    ('days', 'Days'),
    ('weeks', 'Weeks'),
    ('months', 'Months'),
    ('years', 'Years')
)

VISA_TYPES = (
    ('diplomatic', 'Diplomatic'),
    ('official', 'Official'),
    ('employment', 'Employment'),
    ('business', 'Business'),
    ('investment', 'Investment'),
    ('tourist', 'Tourist'),
    ('visitor', 'Visitor'),
    ('study', 'Study'),
    ('transit', 'Transit'),
    ('emergency', 'Emergency')
)

CURRENCY_CHOICES = (
    ('USD', _('United States Dollar')),
    ('EUR', _('Euro')),
    ('ZAR', _('South African Rand')),
    ('GBP', _('British Pound')),
    ('JPY', _('Japanese Yen')),
    ('AUD', _('Australian Dollar')),
    ('CAD', _('Canadian Dollar')),
    ('CHF', _('Swiss Franc')),
    ('CNY', _('Chinese Yuan')),
    ('INR', _('Indian Rupee')),
    ('OTHER', _('Other, specify ...')),

)