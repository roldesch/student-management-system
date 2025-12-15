# application/responses/base_response.py

class BaseResponse:
    """
    Simple base class for use-case response models.
    """

    def __init__(self, success: bool, message: str | None = None, errors: list[str] | None = None):
        self.success = success
        self.message = message
        self.errors = errors or []

    def add_error(self, error: str):
        self.errors.append(error)
        self.success = False