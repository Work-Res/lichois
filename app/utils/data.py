from datetime import date

statuses = [{
    'code': 'New',
    'name': 'NEW',
    'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
    'valid_from': date(2023, 1, 1),
    'valid_to': None
},
    {
        'code': 'draft',
        'name': 'Draft',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'VERIFICATION',
        'name': 'Verification',
        'processes': 'WORK_RESIDENT_PERMIT,residentpermit,visa',
        'valid_from': date(2023, 1, 1),
        'valid_to': None
    },
    {
        'code': 'vetting',
        'name': 'Vetting',
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
    },
    {
        'code': 'final_decision',
        'name': 'FINAL_DECISION',
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
