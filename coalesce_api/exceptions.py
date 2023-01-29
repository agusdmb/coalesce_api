class HealthInsuranceException(Exception):
    pass


class HealthInsuranceAPITimeout(HealthInsuranceException):
    pass


class HealthInsuranceValueError(HealthInsuranceException):
    pass


class HealthInsuranceAPIValidationError(HealthInsuranceException):
    pass
