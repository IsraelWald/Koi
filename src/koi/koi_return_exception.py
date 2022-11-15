from .koi_runtime_error import KoiRuntimeError


class KoiReturnException(KoiRuntimeError):
    """
    This is a hack to return values from Koi functions
    """

    def __init__(self, value):
        super().__init__(None, None)
        self.value = value
