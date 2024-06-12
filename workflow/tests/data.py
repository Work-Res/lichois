from datetime import date

statuses = [{
    'code': 'new',
    'name': 'NEW',
    'processes': 'workpermit,residentpermit,visa',
    'valid_from': date(2023, 1, 1),
    'valid_to': None
},
    {
        'code': 'draft',
        'name': 'DRAFT',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'verification',
        'name': 'VERIFICATION',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'vetting',
        'name': 'VETTING',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'committee_evaluation',
        'name': 'COMMITTEE EVALUATION',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'rejected',
        'name': 'REJECTED',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'accepted',
        'name': 'ACCEPTED',
        'processes': 'workpermit,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    }
]
