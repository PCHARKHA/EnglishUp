# app/scripts/seed_prompts_custom.py
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.prompt import Prompt
from app.core.enums import AgeCategory, ProficiencyLevel, SkillType, DifficultyLevel

# --- Utility function to map proficiency to difficulty ---
def proficiency_to_difficulty(proficiency: ProficiencyLevel) -> DifficultyLevel:
    if proficiency in (ProficiencyLevel.VERY_BASIC, ProficiencyLevel.BASIC):
        return DifficultyLevel.EASY
    if proficiency == ProficiencyLevel.INTERMEDIATE:
        return DifficultyLevel.MEDIUM
    return DifficultyLevel.HARD


# --- Custom prompts dictionary (exactly as provided) ---
PROMPTS = {
    AgeCategory.SCHOOL: {
        ProficiencyLevel.VERY_BASIC: {
            SkillType.GRAMMAR: "Fill in the blanks with simple verbs.",
            SkillType.WRITING: "Write 3 sentences about your school.",
            SkillType.SPEAKING: "Introduce yourself in simple English."
        },
        ProficiencyLevel.BASIC: {
            SkillType.GRAMMAR: "Correct the sentences using past tense.",
            SkillType.WRITING: "Describe your favorite hobby in a short paragraph.",
            SkillType.SPEAKING: "Talk about your daily routine."
        },
        ProficiencyLevel.INTERMEDIATE: {
            SkillType.GRAMMAR: "Identify and correct errors in a short passage.",
            SkillType.WRITING: "Write a letter to a friend inviting them to a party.",
            SkillType.SPEAKING: "Explain a simple process, like making tea."
        },
        ProficiencyLevel.ADVANCED: {
            SkillType.GRAMMAR: "Rewrite sentences using complex clauses.",
            SkillType.WRITING: "Write a short story based on this theme: 'A surprising day.'",
            SkillType.SPEAKING: "Describe your favorite book and why you like it."
        },
        ProficiencyLevel.FLUENT: {
            SkillType.GRAMMAR: "Analyze and correct grammar in a news article.",
            SkillType.WRITING: "Write an essay expressing your opinion on school uniforms.",
            SkillType.SPEAKING: "Discuss a social topic like environmental issues."
        },
    },
    AgeCategory.HIGH_SCHOOL: {
        ProficiencyLevel.VERY_BASIC: {
            SkillType.GRAMMAR: "Simple sentence completion exercises.",
            SkillType.WRITING: "Write 3 sentences about your weekend.",
            SkillType.SPEAKING: "Introduce yourself to a classmate."
        },
        ProficiencyLevel.BASIC: {
            SkillType.GRAMMAR: "Correct simple tense errors in sentences.",
            SkillType.WRITING: "Describe your favorite teacher.",
            SkillType.SPEAKING: "Talk about your daily schedule."
        },
        ProficiencyLevel.INTERMEDIATE: {
            SkillType.GRAMMAR: "Identify grammar mistakes in a short paragraph.",
            SkillType.WRITING: "Write a letter to your friend about a school event.",
            SkillType.SPEAKING: "Explain your favorite hobby in detail."
        },
        ProficiencyLevel.ADVANCED: {
            SkillType.GRAMMAR: "Rewrite sentences using relative clauses and conjunctions.",
            SkillType.WRITING: "Write a short story based on 'An unexpected event.'",
            SkillType.SPEAKING: "Describe your favorite movie plot."
        },
        ProficiencyLevel.FLUENT: {
            SkillType.GRAMMAR: "Analyze and correct grammar in a newspaper article.",
            SkillType.WRITING: "Write an argumentative essay on social media usage.",
            SkillType.SPEAKING: "Discuss the importance of environmental conservation."
        },
    },
    AgeCategory.COLLEGE_PROFESSIONAL: {
        ProficiencyLevel.VERY_BASIC: {
            SkillType.GRAMMAR: "Complete simple sentences with correct verbs.",
            SkillType.WRITING: "Introduce yourself in 5–6 sentences.",
            SkillType.SPEAKING: "Talk about your college life in simple words."
        },
        ProficiencyLevel.BASIC: {
            SkillType.GRAMMAR: "Correct errors in basic paragraph writing.",
            SkillType.WRITING: "Write a short paragraph about your favorite subject.",
            SkillType.SPEAKING: "Explain your daily college routine."
        },
        ProficiencyLevel.INTERMEDIATE: {
            SkillType.GRAMMAR: "Find and correct grammar mistakes in a medium-length text.",
            SkillType.WRITING: "Write a formal email to a professor.",
            SkillType.SPEAKING: "Present a short explanation of a concept you learned recently."
        },
        ProficiencyLevel.ADVANCED: {
            SkillType.GRAMMAR: "Rewrite paragraphs using complex sentence structures.",
            SkillType.WRITING: "Write a reflective essay on a college project.",
            SkillType.SPEAKING: "Discuss your opinion on a current event."
        },
        ProficiencyLevel.FLUENT: {
            SkillType.GRAMMAR: "Analyze advanced grammar in academic texts.",
            SkillType.WRITING: "Write an essay on global issues.",
            SkillType.SPEAKING: "Debate a social or political topic fluently."
        },
    },
    AgeCategory.WORKING_ADULT: {
        ProficiencyLevel.VERY_BASIC: {
            SkillType.GRAMMAR: "Correct simple workplace sentences.",
            SkillType.WRITING: "Introduce yourself at a new job in writing.",
            SkillType.SPEAKING: "Talk about your profession in simple English."
        },
        ProficiencyLevel.BASIC: {
            SkillType.GRAMMAR: "Correct basic errors in emails.",
            SkillType.WRITING: "Write a short email to a colleague.",
            SkillType.SPEAKING: "Explain your daily work schedule."
        },
        ProficiencyLevel.INTERMEDIATE: {
            SkillType.GRAMMAR: "Identify grammar mistakes in a business email.",
            SkillType.WRITING: "Write a report summary in clear English.",
            SkillType.SPEAKING: "Give a short presentation on your work."
        },
        ProficiencyLevel.ADVANCED: {
            SkillType.GRAMMAR: "Rewrite professional documents with complex structures.",
            SkillType.WRITING: "Write a proposal or report on a workplace project.",
            SkillType.SPEAKING: "Discuss work challenges and solutions fluently."
        },
        ProficiencyLevel.FLUENT: {
            SkillType.GRAMMAR: "Analyze and improve grammar in corporate communication.",
            SkillType.WRITING: "Write an essay on leadership or professional development.",
            SkillType.SPEAKING: "Conduct a professional discussion or debate confidently."
        },
    }
}


def seed():
    """
    Seed all prompts into the database.
    """
    db: Session = SessionLocal()
    try:
        for age_category, prof_map in PROMPTS.items():
            for proficiency, skill_map in prof_map.items():
                difficulty = proficiency_to_difficulty(proficiency)

                for skill_type, text in skill_map.items():
                    # Avoid duplicates if running multiple times
                    existing = (
                        db.query(Prompt)
                        .filter_by(
                            age_category=age_category,
                            skill_type=skill_type,
                            difficulty=difficulty,
                            prompt_text=text,
                        )
                        .first()
                    )
                    if not existing:
                        db.add(
                            Prompt(
                                age_category=age_category,
                                skill_type=skill_type,
                                difficulty=difficulty,
                                prompt_text=text,
                            )
                        )

        db.commit()
        print("✅ All prompts seeded successfully")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding prompts: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
