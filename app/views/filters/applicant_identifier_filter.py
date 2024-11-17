from ...models.application_document import ApplicationDocument


class ApplicantIdentifierFilter:

    def filter_by_document_number(self, queryset, name, value):
        try:
            # Get the user application identifier based on the document number
            application_document = ApplicationDocument.objects.get(
                document_number=value
            )

            user_application_identifier = application_document.applicant.user_identifier

            print(f"User application identifier: {user_application_identifier}")

            # Filter the queryset using the user application identifier
            query = queryset.filter(
                application_user__user_identifier=user_application_identifier
            )
            return query
        except ApplicationDocument.DoesNotExist:
            return queryset.none()
