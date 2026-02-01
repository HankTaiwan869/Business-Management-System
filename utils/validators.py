def is_valid_name(input: str) -> bool:
    return input.strip() != ""


def is_valid_number(input: float | int) -> bool:
    return input >= 0
