# app/utils/proficiency.py
from app.core.enums import ProficiencyLevel

def get_proficiency_level(rating: int) -> ProficiencyLevel:
    """
    Maps a numeric proficiency rating (1–5) to a ProficiencyLevel enum.
    
    Args:
        rating (int): User proficiency rating (1–5)
    
    Returns:
        ProficiencyLevel: Corresponding proficiency level
    
    Raises:
        ValueError: If rating is outside 1–5
    """
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")

    mapping = {
        1: ProficiencyLevel.VERY_BASIC,
        2: ProficiencyLevel.BASIC,
        3: ProficiencyLevel.INTERMEDIATE,
        4: ProficiencyLevel.ADVANCED,
        5: ProficiencyLevel.FLUENT,
    }

    return mapping[rating]
