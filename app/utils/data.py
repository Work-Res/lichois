from datetime import date

statuses = [{
    'code': 'new',
    'name': 'NEW',
    'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
    'valid_from': date(2023, 1, 1),
    'valid_to': None
},
    {
        'code': 'draft',
        'name': 'DRAFT',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'verification',
        'name': 'VERIFICATION',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'vetting',
        'name': 'VETTING',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'committee_evaluation',
        'name': 'COMMITTEE EVALUATION',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'rejected',
        'name': 'REJECTED',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'accepted',
        'name': 'ACCEPTED',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    }
]

offices = [
    {
        "name": "Gaborone",
        "code": "01"
    }
]
