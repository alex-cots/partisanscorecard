from django.db.models import TextChoices


class Chamber(TextChoices):
    SENATE = "senate"
    HOUSE = "house"

    @classmethod
    def from_letter(cls, letter: str):
        if letter.lower() == "s":
            return cls.SENATE
        if letter.lower() == "h":
            return cls.HOUSE
        raise ValueError(f"{letter} is not a valid letter abbreviation for Chamber.")

    @classmethod
    def from_full_name(cls, full_name: str):
        if full_name.lower() == "senate":
            return cls.SENATE
        if full_name.lower() == "house of representatives":
            return cls.HOUSE
        raise ValueError(f"{full_name} is not a valid full name for Chamber.")
