
INTEGRATION_TERMS = [
    "integrate",
    "integration",
    "integrates",
    "connect to",
    "connect with",
    "connected to",
    "connects to",
    "sync with",
    "sync to",
    "synchronize with",
    "salesforce",
    "hubspot",
    "google calendar",
]

INTEGRATION_FALLBACK = (
    "I don't have verified information about that integration. "
    "I can arrange a human follow-up to confirm it."
)

FALLBACK_ANSWER = (
    "I don't have verified information to answer that question. "
    "I can arrange a human follow-up to confirm it."
)

PRICING_TERMS = [
    "price",
    "pricing",
    "cost",
    "how much",
    "discount",
    "expensive",
    "cheap",
]

DOCUMENTED_CAPABILITIES = [
    "answer product questions",
    "answers product questions",
    "approved company documents",
    "collects information about prospects",
    "business needs",
    "records lead qualification outcomes",
    "human follow-ups",
    "qualify leads",
    "lead qualification",
    "phone conversations",
    "explains products",
    "answering prospect questions",
    "identifying potential customers",
]

CAPABILITY_QUESTION_TERMS = [
    "does it",
    "does leadpilot",
    "can it",
    "can leadpilot",
    "do you support",
    "does it support",
    "support",
    "automatically",
    "automatic",
    "feature",
    "features",
    "capability",
    "capabilities",
    "able to",
]


def is_integration_question(question: str) -> bool:
    question_lower = question.lower()

    return any(
        term in question_lower
        for term in INTEGRATION_TERMS
    )


def is_capability_question(question: str) -> bool:
    question_lower = question.lower()

    return (
        any(
            term in question_lower
            for term in CAPABILITY_QUESTION_TERMS
        )
        or question_lower.startswith("can ")
        or question_lower.startswith("does ")
        or question_lower.startswith("is it able to")
    )


def has_documented_capability(question: str) -> bool:
    question_lower = question.lower()

    return any(
        capability in question_lower
        for capability in DOCUMENTED_CAPABILITIES
    )
