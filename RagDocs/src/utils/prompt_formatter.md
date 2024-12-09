# PromptTemplate.py

This module provides a `PromptTemplate` class for creating and filling in parameterized prompts.  It uses regular expressions to identify and replace slots within a template string.


## Class: `PromptTemplate`

This class facilitates the creation and population of parameterized prompts.

**Constructor:** `__init__(self, template_string)`

* **Parameters:**
    * `template_string (str)`: The template string containing slots enclosed in double curly braces `{{...}}`.  For example: "What is the capital of {{country}}?".

* **Attributes:**
    * `template_string (str)`: Stores the input template string.
    * `slot_pattern (re.Pattern)`: A compiled regular expression pattern to match slots within the template string.


**Method:** `fill_slots(self, variables)`

* **Parameters:**
    * `variables (dict)`: A dictionary where keys represent slot names (as found within the `{{...}}` placeholders) and values are their corresponding replacements.  Missing keys will result in the original slot placeholder being retained in the output.

* **Returns:**
    * `str`: The filled template string with slots replaced by values from the `variables` dictionary.  If a slot is not found in the `variables` dictionary, the original placeholder (e.g., `{{country}}`) remains in the output.

* **Example:**

```python
template = PromptTemplate("What is the capital of {{country}}?")
variables = {"country": "France"}
filled_template = template.fill_slots(variables)  # filled_template will be "What is the capital of France?"

variables = {"country": "France", "other": "value"}
filled_template = template.fill_slots(variables) # filled_template will be "What is the capital of France?"

variables = {"city": "Paris"} # missing country
filled_template = template.fill_slots(variables) # filled_template will be "What is the capital of {{country}}?"
```

The `fill_slots` method uses a lambda function within `re.sub` to achieve efficient slot replacement.  It handles missing slots gracefully by leaving them in their original placeholder format.
