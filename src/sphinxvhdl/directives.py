def string_list(argument: str, required_amount: int = 0) -> list[str]:
    if argument is None:
        return []
    result_list = [x.strip() for x in argument.split(',')]
    if required_amount != 0 and len(result_list) != required_amount:
        raise ValueError(f"Expected {required_amount} arguments, got {len(result_list)}")
    return result_list


def string_list_required(argument: str, required_amount: int = 0) -> list[str]:
    if argument is None:
        raise ValueError("argument required but none supplied")
    return string_list(argument, required_amount)
