import re


class PromptTemplate:
    def __init__(self, template_string):
        self.template_string = template_string
        self.slot_pattern = re.compile(r"{{(.*?)}}")

    def fill_slots(self, variables):
        def replace_slot(match):
            slot_name = match.group(1).strip()
            return str(variables.get(slot_name, f"{{{slot_name}}}"))

        filled_template = self.slot_pattern.sub(replace_slot, self.template_string)
        return filled_template
