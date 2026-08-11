from src.ranker import rank_resumes


def test_rank_resumes_orders_by_score_and_sets_status():
    results = rank_resumes(
        ["a.pdf", "b.pdf"],
        [0.42, 0.91],
        [{"python"}, {"python", "sql"}],
        [{"sql"}, set()],
        threshold=60,
    )

    assert [result.file_name for result in results] == ["b.pdf", "a.pdf"]
    assert results[0].match_percentage == 91.0
    assert results[0].status == "Shortlist"
    assert results[1].status == "Review"
