

class ApplicationDetailsViewMixin:

    @property
    def non_citizen_identifier(self):
        """Returns the applicant's non_citizen_identifier.
        """
        return self.request.user.non_citizen_identifier

    @property
    def personal_details(self):
        """Returns personal details.
        """
        
        personal_details = {
            'Fullname': f'{self.request.user.first_name} {self.request.user.last_name}',
            'Email': self.request.user.email,
            'Date of Birth': self.request.user.dob,
            'Non Citizen Identifier': self.request.user.non_citizen_identifier}
        return personal_details
    