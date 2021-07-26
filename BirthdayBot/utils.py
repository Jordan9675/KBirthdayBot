def convert_expression_to_hashtag(expression: str) -> str:
    if expression.strip():
        return "#" + "".join(char for char in expression if char.isalnum())
    else:
        return ""
