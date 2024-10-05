

class CrmRequestHandler:

    def __init__(self, crm_request, crm_request_substring_configuration):
        self.crm_request = crm_request
        self.crm_request_substring_configuration = crm_request_substring_configuration

    def group_and_trim_keys(self):
        result = []

        for substring in self.crm_request_substring_configuration:
            # Filter the main_dict to get keys containing the substring
            filtered_dict = {k: v for k, v in self.crm_request.items() if substring in k}

            # Trim the keys in the filtered dictionary
            trimmed_dict = {k.replace(f"{substring}_", ""): v for k, v in filtered_dict.items()}

            # Append the trimmed dict to the result
            result.append({substring: trimmed_dict})

        return result
