
def is_allowed_file(filename: str, allowd_ext: set) -> bool:
    return filename.rsplit(".", 1)[1].lower() in allowd_ext