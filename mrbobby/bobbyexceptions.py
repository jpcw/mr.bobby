"""mr.bobby exceptions module."""


class MrBobbyError(Exception):
    """Base class for errors"""


class ConfigurationError(MrBobbyError):
    """Raised during configuration phase"""


class TemplateConfigurationError(ConfigurationError):
    """Raised reading template configuration"""


class ValidationError(MrBobbyError):
    """Raised during question validation"""


class SkipQuestion(MrBobbyError):
    """Raised during pre_ask_question if we should skip it"""