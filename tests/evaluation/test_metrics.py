import pytest
from generic_rag.evaluation import metrics

def test_precision_at_k_normal():
    retrieved = ["a", "b", "c", "d"]
    relevant = ["b", "d", "e"]
    # k=2: ["a", "b"] -> 1 hit. hits / k = 1/2 = 0.5
    assert metrics.precision_at_k(retrieved, relevant, 2) == 0.5
    # k=5: ["a", "b", "c", "d"] -> 2 hits. hits / k = 2/5 = 0.4
    assert metrics.precision_at_k(retrieved, relevant, 5) == 0.4

def test_precision_at_k_empty():
    assert metrics.precision_at_k([], ["a"], 1) == 0.0
    assert metrics.precision_at_k(["a"], [], 1) == 0.0
    assert metrics.precision_at_k(["a"], ["a"], 0) == 0.0

def test_recall_at_k_normal():
    retrieved = ["a", "b", "c", "d"]
    relevant = ["b", "d", "e"]
    # k=2: ["a", "b"] -> 1 hit. hits / total_relevant = 1/3
    assert metrics.recall_at_k(retrieved, relevant, 2) == pytest.approx(1/3)
    # k=4: 2 hits. 2/3
    assert metrics.recall_at_k(retrieved, relevant, 4) == pytest.approx(2/3)

def test_hit_at_k():
    retrieved = ["a", "b", "c"]
    relevant = ["c", "d"]
    assert metrics.hit_at_k(retrieved, relevant, 2) == 0.0
    assert metrics.hit_at_k(retrieved, relevant, 3) == 1.0

def test_reciprocal_rank_at_k():
    relevant = ["c"]
    # Hit at pos 3, k=2 -> 0.0
    assert metrics.reciprocal_rank_at_k(["a", "b", "c"], relevant, 2) == 0.0
    # Hit at pos 3, k=3 -> 1/3
    assert metrics.reciprocal_rank_at_k(["a", "b", "c"], relevant, 3) == pytest.approx(1/3)
    # Hit at pos 1, k=1 -> 1.0
    assert metrics.reciprocal_rank_at_k(["c", "a", "b"], relevant, 1) == 1.0

def test_reciprocal_rank():
    relevant = ["c"]
    assert metrics.reciprocal_rank(["a", "b", "c"], relevant) == 1/3
    assert metrics.reciprocal_rank(["c", "a", "b"], relevant) == 1.0
    assert metrics.reciprocal_rank(["a", "b"], relevant) == 0.0

def test_mrr():
    ret_lists = [["a", "b"], ["c", "a"]]
    rel_lists = [["b"], ["c"]]
    # RR1 = 1/2, RR2 = 1/1. MRR = (0.5 + 1.0) / 2 = 0.75
    assert metrics.mrr(ret_lists, rel_lists) == 0.75

def test_ndcg_at_k_perfect():
    retrieved = ["a", "b", "c"]
    relevance_map = {"a": 3.0, "b": 2.0, "c": 1.0}
    # Ideal order retrieved. nDCG should be 1.0
    assert metrics.ndcg_at_k(retrieved, relevance_map, 3) == 1.0

def test_ndcg_at_k_partial():
    retrieved = ["c", "b", "a"]
    relevance_map = {"a": 3.0, "b": 2.0, "c": 1.0}
    # DCG = 1/log2(2) + 2/log2(3) + 3/log2(4) = 1 + 1.2618 + 1.5 = 3.7618
    # IDCG = 3/log2(2) + 2/log2(3) + 1/log2(4) = 3 + 1.2618 + 0.5 = 4.7618
    # nDCG = 3.7618 / 4.7618 = 0.7899
    assert metrics.ndcg_at_k(retrieved, relevance_map, 3) == pytest.approx(0.7899, abs=1e-4)

def test_citation_coverage():
    assert metrics.citation_coverage(["c1", "c2"], ["c1", "c3"]) == 0.5
    assert metrics.citation_coverage([], ["c1"]) == 0.0
    assert metrics.citation_coverage(["c1"], []) == 0.0

def test_context_coverage():
    assert metrics.context_coverage(["chunk1", "chunk2"], ["chunk2", "chunk3"]) == 0.5
