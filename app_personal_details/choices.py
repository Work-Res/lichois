from django.utils.translation import gettext as _

EDUCATION_LEVELS = (
    ("high_school", _("High School")),
    ("certificate", _("Certificate/Vocational")),
    ("associate_degree", _("Associate Degree")),
    ("diploma", _("Diploma/ Technical Degree")),
    ("professional_degree", _("Degree/Professional Degree")),
    ("masters_degree", _("Master's Degree")),
    ("doctorate", _("Doctorate")),
    ("professor", _("Professor")),
    ("Other", _("Other: Specify other education")),
)


GENDER = (("male", "Male"), ("female", "Female"), ("other", "OTHER"))

MARITAL_STATUS = (
    ("single", "Single"),
    ("married", "Married"),
    ("widowed", "Widowed"),
    ("separated", "Separated"),
    ("divorced", "Divorced"),
)

PERSON_TYPE = (
    ('applicant', 'Applicant'),
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('child', 'Child'),
    ('guardian', 'Guardian'),
    ('sponsor', 'Sponsor'),
    ('witness', 'Witness'),
    ('declarant', 'Declarant'),
    ('adoptive_parent', 'Adoptive Parent'),
    ('subscriber', 'Subscriber'),
)
