from django import template

register = template.Library()

@register.filter
def format_large_number(value):
    """
    Converts a number to K (thousand), M (million), or B (billion) format without trailing '.0'.
    """
    try:
        num = float(value)
        if num >= 1_000_000_000:
            formatted = num / 1_000_000_000
            suffix = " bn"
        elif num >= 1_000_000:
            formatted = num / 1_000_000
            suffix = " mn"
        elif num >= 1_000:
            formatted = num / 1_000
            suffix = " k"
        else:
            return f"{int(num)}"  # For numbers below 1K, return as is

        # Remove '.0' if it's a whole number
        if formatted.is_integer():
            return f"{int(formatted)}{suffix}"
        else:
            return f"{formatted:.1f}{suffix}"  # Keep one decimal place for non-integers

    except (ValueError, TypeError):
        return value  # Return the original value if conversion fails
