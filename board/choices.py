PRESENT = 'present'
ABSENT = 'absent'
ENDED = 'ended'
STARTED = 'started'
APPROVED = 'approved'
ACCEPTED = 'accepted'
REJECTED = 'rejected'
PENDING = 'pending'
CANCELLED = 'cancelled'
SCHEDULED = 'scheduled'
ON_GOING = 'on_going'
COMPLETED = 'completed'
DEFERRED = 'deferred'

ATTENDANCE_STATUS = (
    (ABSENT, 'Absent'),
    (PRESENT, 'Present'),
)

DECISION_OUTCOME = (
    (ACCEPTED, 'Accepted'),
    (DEFERRED, 'Deferred'),
    (REJECTED, 'Rejected')
)

BOARD_ROLES = (
	('chair_person', 'Chairperson'),
	('secretary', 'Secretary'),
	('member', 'Member'),
)

BOARD_MEETING_STATUS = (
	(SCHEDULED, 'Scheduled'),
	(CANCELLED, 'Cancelled'),
	(ON_GOING, 'Ongoing'),
	(COMPLETED, 'Completed'),
)

BOARD_MEETING_TYPES = (
	('virtual', 'Virtual'),
	('physical', 'Physical'),
)

AGENDA_STATUS = (
	('pending', 'Pending'),
	('discussed', 'Discussed'),
	('completed', 'Completed'),
)


VOTE_STATUS = (
	(APPROVED, 'Approved'),
	(REJECTED, 'Rejected'),
)

VOTING_PROCESS_STATUS = (
	(STARTED, 'Started'),
	(ENDED, 'Ended'),
)

BOARD_RESOLUTION = (
    ('refrain', 'Refrain'),
    ('vote', 'Vote'),
)

INTEREST_LEVEL = (
	('investment', 'Investment'),
	('business_position', 'Business Position'),
	('real_property', 'Real Property'),
	('personal_financial_effect', 'Personal Financial Effect'),
	('other', 'Other'),
)

MEETING_INVITATION_STATUS = (
	(APPROVED, 'Approved'),
	(REJECTED, 'Rejected'),
	(PENDING, 'Pending'),
)



