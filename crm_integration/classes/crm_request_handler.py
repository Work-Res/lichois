from django.apps import apps


class CrmRequestHandler:

    def __init__(self, crm_request):
        self.crm_request = crm_request

    def group_and_trim_keys(self):
        result = []

        for substring in self.crm_req_substring_config:
            # Filter the main_dict to get keys containing the substring
            filtered_dict = {k: v for k, v in self.crm_request.items() if substring in k}

            # Trim the keys in the filtered dictionary
            trimmed_dict = {k.replace(f"{substring}_", ""): v for k, v in filtered_dict.items()}

            # Append the trimmed dict to the result
            result.append({substring: trimmed_dict})

        return result

    @property
    def crm_req_substring_config(self):
        """Returns apps and models list.
        """

        # Loop through all installed apps
        substrings = []
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            # Loop through all models in the app
            for model in app_config.get_models():
                model_name = model.__name__
                # Join app label and model name with an underscore
                substrings.append(f"{app_label}_{model_name}")
        return substrings