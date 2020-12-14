class TokenizationError(Exception):
    """Custom exception when failing parses."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)
