from django.core.exceptions import ValidationError
from django.db import transaction
from citizenship.models.board import InterviewResponse, Interview, InterviewQuestion, BoardMember


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
    def update_interview_response(response_id, response=None, score=None):
        try:
            interview_response = InterviewResponse.objects.get(id=response_id)
            if response is not None:
                interview_response.response = response
            if score is not None:
                interview_response.score = score
            interview_response.is_marked = True
            interview_response.save()
            return interview_response
        except InterviewResponse.DoesNotExist:
            raise ValidationError("Interview response does not exist.")
        except Exception as e:
            raise ValidationError(f"Error updating interview response: {str(e)}")

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
