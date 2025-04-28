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
    
@register.filter
def split_by_period(value):
    return [s.strip() + '.' for s in value.split('.') if s.strip()]

@register.filter
def to_million(value):
    try:
        value = float(value)
        if value >= 1_000_000_000_000:
            return f"{value / 1_000_000_000_000:.2f} tn"
        elif value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f} bn"
        else:
            return f"{value / 1_000_000:.2f} mn"
    except (ValueError, TypeError):
        return value
    
@register.filter
def format_percent(value):
    """
    Rounds a float to 2 decimal places and appends a % sign.
    Example: 2.542700299 -> '2.54%'
    """
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return value
