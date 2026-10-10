
from app.llm import generate_answer

context = (
    "LeadPilot AI is an AI-powered voice agent that helps businesses "
    "qualify leads through phone conversations."
)

question = "What does LeadPilot AI do?"

answer = generate_answer(question, context)

print("\nQuestion:", question)
print("Answer:", answer)
