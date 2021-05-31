from dataclasses import dataclass


@dataclass(frozen=True)
class Username:
    __value: str

    def validate(self):
        if self.__value.strip() == "":
            raise ValueError("username could not be empty string")

    def __post_init__(self):
        self.validate()

    def __str__(self):
        return self.__value

    def __repr__(self):
        return f"Username({self.__str__()})"

    def __eq__(self, other):
        return self.__value == other.__value

    def __hash__(self):
        return hash(self.__value)

    @property
    def value(self):
        return self.__value
