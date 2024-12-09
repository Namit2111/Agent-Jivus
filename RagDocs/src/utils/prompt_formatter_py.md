# PromptTemplate Class Documentation

This class provides a simple mechanism for creating and filling parameterized prompts or templates.  It uses regular expressions to identify and replace placeholders within a template string.

## Class: `PromptTemplate`

**Purpose:** Creates and manages parameterized prompts, allowing for dynamic substitution of variables.

**Constructor:** `__init__(self, template_string)`

* **Parameters:**
    * `template_string (str)`: The template string containing placeholders in the format `{{variable_name}}`.

* **Attributes:**
    * `template_string (str)`: The original template string.
    * `slot_pattern (re.Pattern)`: A compiled regular expression pattern to match placeholders.


**Methods:**

**`fill_slots(self, variables)`**

* **Parameters:**
    * `variables (dict)`: A dictionary where keys are the variable names (as found within the `{{...}}` placeholders in `template_string`) and values are their corresponding substitutions.

* **Returns:**
    * `str`: The filled template string with placeholders replaced by values from the `variables` dictionary.  If a placeholder's corresponding key is not found in `variables`, the placeholder itself (including the curly braces) is retained in the output string.

* **Functionality:** This method iterates through the `template_string` using the compiled regular expression `slot_pattern`. For each match (a placeholder), it attempts to retrieve the corresponding value from the `variables` dictionary. If a value is found, it replaces the placeholder; otherwise, it leaves the placeholder unchanged.


**Example Usage:**

```python
from prompt_template import PromptTemplate

template = PromptTemplate("My name is {{name}} and I am {{age}} years old.")
filled_template = template.fill_slots({"name": "Alice", "age": 30})
print(filled_template)  # Output: My name is Alice and I am 30 years old.

filled_template = template.fill_slots({"name": "Bob"})
print(filled_template)  # Output: My name is Bob and I am {{age}} years old.

```
