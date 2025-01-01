import re


def fill_template(config: list | dict, template: str) -> str:
    # Check if we have a list and need to duplicate the template
    if isinstance(config, list):
        # Call function on template for each item
        fills_list = [fill_template(x, template) for x in config]

        # Concatenate all results
        concat_str = "".join(fills_list)

        # Return concatenated string
        return concat_str

    # Check if we have a dictionary and can apply all replacements
    if isinstance(config, dict):
        # Call function for each key-value pair on the same string
        for k, v in config.items():

            # Define pattern for splitting the template at tags
            pattern = rf"(.*?)^[ \t]*% <{k}>\n(.*?)^[ \t]*% </{k}>\n(.*)"

            # Match pattern on the template
            template_match = re.match(pattern, template, re.MULTILINE | re.DOTALL)

            # Continue if no match
            if not template_match:
                continue

            # Get split results
            template_before, template_middle, template_after = template_match.groups()

            if not isinstance(v, dict) and not isinstance(v, list):
                # Fill value
                pattern = rf"(.*^\s*)(.*?)(\% {k}$.*)"

                # Match pattern on the template
                template_middle_match = re.match(
                    pattern, template_middle, re.MULTILINE | re.DOTALL
                )

                # Continue if no match
                if not template_middle_match:
                    continue

                # Get split results
                (
                    template_middle_before,
                    template_middle_middle,
                    template_middle_after,
                ) = template_middle_match.groups()

                # Replace middle
                template_middle = (
                    template_middle_before + str(v).strip("\n") + template_middle_after
                )

            else:
                # Filled middle
                template_middle = fill_template(v, template_middle)

            # Joined
            template = template_before + template_middle + template_after

        # Return
        return template


def clean_unused_tags(template: str) -> str:
    # Define pattern for tags
    pattern = r"^[ \t]*?\% <([^>]+)>.*?[ \t]*?\% </\1>\n"

    # Replace with an empty string
    template_new = re.sub(pattern, "", template, flags=re.MULTILINE | re.DOTALL)

    # Return
    return template_new
