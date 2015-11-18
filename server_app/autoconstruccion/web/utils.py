

def get_image_from_file_field(file_field, request):
    """
    Extract a file of a FileField and a request and returns a reference to a bytearray
    :param file_field: FileField from Flask-WTF
    :param request: the request containing the file
    :return: a buffer suitable to assign a SQLAlchemy binary or None.
    """
    if file_field.has_file():
        storage = request.files['image']
        file = storage.stream.getbuffer()
        return file
    else:
        return None
