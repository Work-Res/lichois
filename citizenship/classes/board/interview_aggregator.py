from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import InterviewResponse, ScoreSheet, ScoreSheetDetail, InterviewQuestion


class InterviewAggregator:

    @staticmethod
    @transaction.atomic
    def aggregate_and_create_details(score_sheet_id, interview_question_id=None):
        try:
            score_sheet = ScoreSheet.objects.get(id=score_sheet_id)
            interview = score_sheet.interview

            # Filter responses by interview question if provided
            if interview_question_id:
                responses = InterviewResponse.objects.filter(interview=interview, question_id=interview_question_id)
            else:
                responses = InterviewResponse.objects.filter(interview=interview)

            if not responses.exists():
                raise ValidationError("No interview responses found for this interview.")

            question_scores = {}

            for response in responses:
                question_id = response.question.id
                if question_id not in question_scores:
                    question_scores[question_id] = {
                        "total_score": 0,
                        "responses": []
                    }
                if response.score is not None:
                    question_scores[question_id]["total_score"] += response.score
                    question_scores[question_id]["responses"].append(response)

            for question_id, data in question_scores.items():
                total_score = data["total_score"]
                num_responses = len(data["responses"])
                average_score = total_score / num_responses if num_responses > 0 else 0

                aggregated_responses = [
                    {
                        "member_id": response.member.id,
                        "response": response.response,
                        "score": response.score
                    } for response in data["responses"]
                ]

                ScoreSheetDetail.objects.create(
                    score_sheet=score_sheet,
                    question=InterviewQuestion.objects.get(id=question_id),
                    aggregated_score=average_score,
                    aggregated_responses=aggregated_responses
                )
        except ScoreSheet.DoesNotExist:
            raise ValidationError("ScoreSheet does not exist.")
        except InterviewQuestion.DoesNotExist:
            raise ValidationError("InterviewQuestion does not exist.")
        except Exception as e:
            raise ValidationError(f"Error in aggregation and creation of ScoreSheetDetail: {str(e)}")
