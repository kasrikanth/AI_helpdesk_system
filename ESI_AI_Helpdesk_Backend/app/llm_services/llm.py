from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.utils.config import OPENAI_API_KEY
from app.llm_services.prompts import PROMPT_TEMPLATE
from typing import List, Dict, Any

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

def generate_answer(question, docs):
    context = "\n\n".join(
        f"[{d.metadata['kb_id']} | v{d.metadata['version']}]\n{d.page_content}"
        for d in docs)
    
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content

def compute_response_confidence(docs: List[Dict[str, Any]], response_text: str) -> float:
    # No documents → zero confidence
    if not docs:
        return 0.0

    negative_indicators = {
        "not covered in the knowledge base","not in the knowledge base","no information",
        "cannot find","is not available", "i don't have","missing from the knowledge base",
        "no record available","information not present","unavailable in current data","not documented",
        "no entry found","data not available","not stored in the system","no matching information",
        "knowledge gap","not tracked","no reference found","absent from records","cannot locate",
        "no relevant data", "not part of the database", "no support information","no details available"
    }

    response_lower = response_text.lower()

    # If the answer clearly signals missing knowledge
    if any(flag in response_lower for flag in negative_indicators):
        return 0.0

    # Extract similarity scores safely
    similarity_scores = [entry.get("similarity", 0.0) for entry in docs]

    if not similarity_scores:
        return 0.0

    mean_score = sum(similarity_scores) / len(similarity_scores)
    highest_score = max(similarity_scores)

    # Base confidence derived from average similarity
    if mean_score >= 0.35:
        base_conf = 0.95
    elif mean_score >= 0.30:
        base_conf = 0.88
    elif mean_score >= 0.25:
        base_conf = 0.82
    elif mean_score >= 0.20:
        base_conf = 0.72
    elif mean_score >= 0.15:
        base_conf = 0.60
    else:
        base_conf = max(mean_score * 2.5, 0.40)

    # Bonus for multiple strong matches
    strong_count = sum(1 for score in similarity_scores if score > 0.25)
    if strong_count >= 2:
        base_conf += 0.06
    if strong_count >= 3:
        base_conf += 0.04

    # Bonus for very high top match
    if highest_score > 0.40:
        base_conf += 0.05

    # Signals suggesting grounded explanation
    reference_clues = [
        "according to", "documented in", "as outlined",
        "per the", "kb-", "steps:", "here's how",
        "follow these steps", "the process",
        "in the knowledge base", "provided in"
    ]

    clue_hits = sum(1 for clue in reference_clues if clue in response_lower)
    if clue_hits >= 2:
        base_conf += 0.04

    # Penalize extremely short answers
    if len(response_text.strip()) < 50:
        base_conf -= 0.10

    # Enforce lower bound if similarity is decent
    if mean_score >= 0.25 and base_conf < 0.80:
        base_conf = 0.80

    # Clamp value between 0 and 1
    base_conf = min(max(base_conf, 0.0), 1.0)

    return round(base_conf, 2)



