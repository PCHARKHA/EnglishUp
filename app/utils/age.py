
from app.core.enums import AgeCategory

def get_age_category(age: int) -> AgeCategory:
    """
    Maps a numeric age to an AgeCategory enum.
    Args:age (int): User age
    Returns:
        AgeCategory: Corresponding age category
    Raises:
        ValueError: If age is negative or outside supported range
    """
    if age < 0:
        raise ValueError("Age cannot be negative")

    if 12 <= age <= 15:
        return AgeCategory.SCHOOL
    elif 16 <= age <= 18:
        return AgeCategory.HIGH_SCHOOL
    elif 19 <= age <= 25:
        return AgeCategory.COLLEGE_PROFESSIONAL
    elif 26 <= age <= 60:
        return AgeCategory.WORKING_ADULT
    else:
        raise ValueError("Age outside supported range (12–60)")
