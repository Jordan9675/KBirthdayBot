def convert_expression_to_hashtag(expression: str) -> str:
    return "#" + "".join(char for char in expression if char.isalnum())
