import math
from typing import Dict, List

def precision_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if k <= 0 or not relevant_ids:
        return 0.0
    
    if not retrieved_ids:
        return 0.0
    
    top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    hits = sum(1 for idx in top_k if idx in relevant_set)
    
    return hits / k

def recall_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if k <= 0 or not retrieved_ids or not relevant_ids:
        return 0.0
    
    top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    hits = sum(1 for idx in top_k if idx in relevant_set)
    
    return hits / len(relevant_ids)

def hit_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if k <= 0 or not retrieved_ids or not relevant_ids:
        return 0.0
    
    top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    
    for idx in top_k:
        if idx in relevant_set:
            return 1.0
    return 0.0

def reciprocal_rank_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if k <= 0 or not retrieved_ids or not relevant_ids:
        return 0.0
    
    top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    for i, idx in enumerate(top_k):
        if idx in relevant_set:
            return 1.0 / (i + 1)
    return 0.0

def reciprocal_rank(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
    if not retrieved_ids or not relevant_ids:
        return 0.0
    
    relevant_set = set(relevant_ids)
    for i, idx in enumerate(retrieved_ids):
        if idx in relevant_set:
            return 1.0 / (i + 1)
    return 0.0

def mrr(retrieved_lists: List[List[str]], relevant_lists: List[List[str]]) -> float:
    if not retrieved_lists or not relevant_lists or len(retrieved_lists) != len(relevant_lists):
        return 0.0
    
    rr_sum = sum(reciprocal_rank(ret, rel) for ret, rel in zip(retrieved_lists, relevant_lists))
    return rr_sum / len(retrieved_lists)

def dcg_at_k(retrieved_ids: List[str], relevance_map: Dict[str, float], k: int) -> float:
    if k <= 0 or not retrieved_ids:
        return 0.0
    
    top_k = retrieved_ids[:k]
    dcg = 0.0
    for i, idx in enumerate(top_k):
        relevance = relevance_map.get(idx, 0.0)
        dcg += relevance / math.log2(i + 2)
    return dcg

def ndcg_at_k(retrieved_ids: List[str], relevance_map: Dict[str, float], k: int) -> float:
    if k <= 0 or not retrieved_ids or not relevance_map:
        return 0.0
    
    actual_dcg = dcg_at_k(retrieved_ids, relevance_map, k)
    
    # Calculate IDCG (Ideal DCG)
    # Sort all relevant items by their relevance in descending order
    sorted_relevances = sorted(relevance_map.values(), reverse=True)
    ideal_dcg = 0.0
    for i, rel in enumerate(sorted_relevances[:k]):
        ideal_dcg += rel / math.log2(i + 2)
    
    if ideal_dcg == 0:
        return 0.0
    
    return actual_dcg / ideal_dcg

def citation_coverage(citation_ids: List[str], expected_ids: List[str]) -> float:
    if not expected_ids:
        return 0.0
    
    if not citation_ids:
        return 0.0
    
    citation_set = set(citation_ids)
    hits = sum(1 for idx in expected_ids if idx in citation_set)
    return hits / len(expected_ids)

def context_coverage(context_chunk_ids: List[str], relevant_ids: List[str]) -> float:
    if not relevant_ids:
        return 0.0
    
    if not context_chunk_ids:
        return 0.0
    
    context_set = set(context_chunk_ids)
    hits = sum(1 for idx in relevant_ids if idx in context_set)
    return hits / len(relevant_ids)
