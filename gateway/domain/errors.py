class DomainError(Exception):
    pass


class DuplicateTestCaseInput(DomainError):
    pass


class ValidationTestCaseError(DomainError):
    pass
