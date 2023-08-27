from rest.climbs.constants import CLIMBING_GRADE_SCORES


def test_score_climb():
    score = CLIMBING_GRADE_SCORES.get("5.10a")
    assert score == 10.0
