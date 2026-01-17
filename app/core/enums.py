from enum import Enum

class AgeCategory(str, Enum):
    SCHOOL = "school"           #12 -15
    HIGH_SCHOOL = "high_school" #16-18
    COLLEGE_PROFESSIONAL = "college_professional" #19-25
    WORKING_ADULT = "working_adult" #26-60

class ProficiencyLevel(str, Enum):
    VERY_BASIC = "very_basic"    # rating 1
    BASIC = "basic"              # rating 2
    INTERMEDIATE = "intermediate" # rating 3
    ADVANCED = "advanced"        # rating 4
    FLUENT = "fluent"            # rating 5

class SkillType(str, Enum):
    GRAMMAR = "grammar"
    WRITING = "writing"
    SPEAKING = "speaking"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"