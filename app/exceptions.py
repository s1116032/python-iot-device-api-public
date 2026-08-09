class AppError(Exception):
    """應用程式基礎例外。"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """資源不存在。"""


class DeviceNotFoundError(NotFoundError):
    """設備不存在。"""


class ConflictError(AppError):
    """資源衝突。"""


class DeviceCodeAlreadyExistsError(ConflictError):
    """設備編號已存在。"""


class InvalidParameterError(AppError):
    """查詢參數或輸入參數不合法。"""
