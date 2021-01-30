def picture_to_html(picture: str) -> str:
    return "data:image/png;base64, {picture_code}".format(picture_code=picture)
