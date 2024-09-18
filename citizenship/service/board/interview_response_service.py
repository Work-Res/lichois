import logging

from django.core.exceptions import ValidationError
from django.db import transaction

from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse, Interview, InterviewQuestion, BoardMember

logger = logging.getLogger(__name__)


class InterviewResponseService:

    @staticmethod
    @transaction.atomic
    def create_interview_response(interview_id, question_id, member_id, response, score=None):
        try:
            interview = Interview.objects.get(id=interview_id)
            question = InterviewQuestion.objects.get(id=question_id)
            member = BoardMember.objects.get(id=member_id)
            interview_response = InterviewResponse.objects.create(
                interview=interview,
                question=question,
                member=member,
                response=response,
                score=score
            )
            return interview_response
        except Interview.DoesNotExist:
            raise ValidationError("Interview does not exist.")
        except InterviewQuestion.DoesNotExist:
            raise ValidationError("Interview question does not exist.")
        except BoardMember.DoesNotExist:
            raise ValidationError("Board member does not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating interview response: {str(e)}")

    @staticmethod
    def get_interview_response(response_id):
        try:
            interview_response = InterviewResponse.objects.get(id=response_id)
            return interview_response
        except InterviewResponse.DoesNotExist:
            raise ValidationError("Interview response does not exist.")

    @staticmethod
    @transaction.atomic
    def update_interview_response(response_id, data):
        try:
            interview_response = InterviewResponse.objects.get(id=response_id)
            serializer = InterviewResponseSerializer(interview_response, data=data, partial=True)

            if serializer.is_valid():
                for key, value in data.items():
                    setattr(interview_response, key, value)
                interview_response.is_marked = True
                interview_response.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)

        except InterviewResponse.DoesNotExist:
            raise ValidationError("Interview response does not exist.")
        except Exception as e:
            raise ValidationError(f"Error updating interview response: {str(e)}")

    @staticmethod
    @transaction.atomic
    def bulk_update_interview_responses(updates):
        updated_responses = []
        errors = []

        logger.info("Starting bulk update of interview responses.")

        for update in updates:
            response_id = update.get('response_id')
            data = update.get('data', {})

            logger.info(f"Processing update for response ID: {response_id} with data: {data}")

            try:
                # Fetch the InterviewResponse instance
                interview_response = InterviewResponse.objects.get(id=response_id)
                logger.info(f"Found interview response with ID: {response_id}")

                # Serialize the interview response data
                serializer = InterviewResponseSerializer(interview_response, data=data, partial=True)

                if serializer.is_valid():
                    # Log field changes
                    for key, value in data.items():
                        logger.debug(f"Updating field {key} to {value} for response ID: {response_id}")
                        setattr(interview_response, key, value)

                    # Mark as completed and save
                    interview_response.is_marked = True
                    interview_response.save()
                    logger.info(f"Successfully updated interview response with ID: {response_id}")

                    updated_responses.append(serializer.data)
                else:
                    logger.warning(f"Validation failed for response ID: {response_id}. Errors: {serializer.errors}")
                    errors.append({response_id: serializer.errors})

            except InterviewResponse.DoesNotExist:
                logger.error(f"Interview response with ID: {response_id} does not exist.")
                errors.append({response_id: "Interview response does not exist."})

            except Exception as e:
                logger.error(f"Unexpected error occurred while updating response ID: {response_id}. Error: {str(e)}", exc_info=True)
                errors.append({response_id: f"Error updating interview response: {str(e)}"})

        if errors:
            # Convert the list of error dictionaries into a single dictionary
            combined_errors = {}
            for error_dict in errors:
                combined_errors.update(error_dict)

            logger.error(f"Bulk update encountered errors: {combined_errors}")
            return combined_errors, False

        logger.info("Bulk update of interview responses completed successfully.")
        return updated_responses, True

    @staticmethod
    @transaction.atomic
    def delete_interview_response(response_id):
        try:
            interview_response = InterviewResponse.objects.get(id=response_id)
            interview_response.delete()
            return True
        except InterviewResponse.DoesNotExist:
            raise ValidationError("Interview response does not exist.")
        except Exception as e:
            raise ValidationError(f"Error deleting interview response: {str(e)}")

    @staticmethod
    def list_interview_responses(interview_id=None, member_id=None, question_id=None):
        try:
            filters = {}
            if interview_id:
                filters['interview_id'] = interview_id
            if member_id:
                filters['member_id'] = member_id
            if question_id:
                filters['question_id'] = question_id

            return InterviewResponse.objects.filter(**filters)
        except Exception as e:
            raise ValidationError(f"Error listing interview responses: {str(e)}")

    @staticmethod
    @transaction.atomic
    def create_responses_for_questions(interview_id, question_ids, member_ids):
        try:
            interview = Interview.objects.get(id=interview_id)
            responses = []
            for question_id in question_ids:
                question = InterviewQuestion.objects.get(id=question_id)
                for member_id in member_ids:
                    member = BoardMember.objects.get(id=member_id)
                    response = InterviewResponse.objects.create(
                        interview=interview,
                        question=question,
                        member=member,
                        response="",  # Initialize with an empty response
                        score=None
                    )
                    responses.append(response)
            return responses
        except Interview.DoesNotExist:
            raise ValidationError("Interview does not exist.")
        except InterviewQuestion.DoesNotExist:
            raise ValidationError("One or more interview questions do not exist.")
        except BoardMember.DoesNotExist:
            raise ValidationError("One or more board members do not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating interview responses: {str(e)}")

    @staticmethod
    @transaction.atomic
    def delete_all_responses_for_member(member_id):
        try:
            member = BoardMember.objects.get(id=member_id)
            InterviewResponse.objects.filter(member=member).delete()
            return True
        except BoardMember.DoesNotExist:
            raise ValidationError("Board member does not exist.")
        except Exception as e:
            raise ValidationError(f"Error deleting interview responses for member: {str(e)}")
