from typing import Dict

from app.api.common.web import APIResponse, APIMessage


class AssessmentValidator:

    def __init__(self, assessment, rules: Dict = None):
        self.assessment = assessment
        self.rules = rules
        self.response = APIResponse()
        self.exclude_fields = ["maximum_points", "pass_mark"]

    def validate_total_marks(self):
        max_marks = self.rules.get("maximum_points")
        if int(self.assessment.total) > int(max_marks):
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message=f"The assessment totals are incorrect",
                    details=f"The assessment totals are incorrect, specified total: {self.assessment} "
                            f"expected to less or equal to : {max_marks}"
                ).to_dict()
            )

    def validate_main_sections(self):
        for prop, _ in self.rules.items():
            if prop in self.exclude_fields:
                continue
            if not self.check_is_within_expected_marks(prop):
                form_value = getattr(self.assessment, prop)
                max_value = self.rules.get(prop)
                self.validation_range_message(form_value=form_value, max_value=max_value, prop=prop)

    def validate_totals(self):
        pass

    def check_is_within_expected_marks(self, key=None):
        form_value = getattr(self.assessment, key)
        max_value = self.rules.get(key)
        if int(form_value) <= int(max_value):
            return True
        else:
            return False

    def validation_range_message(self, form_value=None, max_value=None, prop=None):
        self.response.messages.append(
            APIMessage(
                code=400,
                message=f"The assessment {prop} is not within the expected range.",
                details=f"The assessment {prop} is not within the expected range. form value: {form_value}, "
                        f"expected range, between 0 and {max_value}"
            ).to_dict()
        )

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.validate_total_marks()
        self.validate_main_sections()
        return True if len(self.response.messages) == 0 else False
