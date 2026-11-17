"""Тесты приложения для распределения по возрасту"""
import pytest

from src.lab3_tasks.task2.main import AgeGroup, Respondent, SurveyGrouper


def test_age_group_labels():
    """Проверка обозначения возрастных групп"""
    assert AgeGroup(0, 18).label == "0-18"
    assert AgeGroup(19, 25).label == "19-25"
    assert AgeGroup(101).label == "101+"


def test_age_group_contains():
    """Проверка принадлежности к группе"""
    group = AgeGroup(19, 25)

    assert group.contains(19)
    assert group.contains(25)
    assert not group.contains(18)
    assert not group.contains(26)


def test_respondent_distribution():
    """Проверка распределения по группам"""
    grouper = SurveyGrouper([18, 25, 35])

    grouper.add_respondent(Respondent("Иванов Иван Иванович", 15))
    grouper.add_respondent(Respondent("Петров Петр Петрович", 22))
    grouper.add_respondent(Respondent("Сидоров Сидор Сидорович", 30))

    assert grouper.get_result() == [
        "26-35: Сидоров Сидор Сидорович (30)",
        "19-25: Петров Петр Петрович (22)",
        "0-18: Иванов Иван Иванович (15)",
    ]


def test_sorting_respondents():
    """Проверка сортировки по возрасту и ФИО"""
    group = AgeGroup(0, 100)

    group.add(Respondent("Петров Петр Петрович", 20))
    group.add(Respondent("Иванов Иван Иванович", 25))
    group.add(Respondent("Сидоров Сидор Сидорович", 20))

    assert group.format() == (
        "0-100: Иванов Иван Иванович (25), "
        "Петров Петр Петрович (20), "
        "Сидоров Сидор Сидорович (20)"
    )


def test_empty_groups_are_not_displayed():
    """Проверка что пустые группы не попадают в результ"""
    grouper = SurveyGrouper([18, 25, 35])

    grouper.add_respondent(Respondent("Иванов Иван Иванович", 15))

    assert grouper.get_result() == ["0-18: Иванов Иван Иванович (15)"]


def test_last_group():
    """Проверяет группу для людей старше последней границы."""
    grouper = SurveyGrouper([18, 25])
    grouper.add_respondent(Respondent("Иванов Иван Иванович", 105))
    assert grouper.get_result() == ["26+: Иванов Иван Иванович (105)"]


def test_invalid_boundaries():
    """Проверка обработки неправильных границ"""
    with pytest.raises(ValueError):
        SurveyGrouper([])
    with pytest.raises(ValueError):
        SurveyGrouper([18, 18, 25])
    with pytest.raises(ValueError):
        SurveyGrouper([25, 18])
    with pytest.raises(ValueError):
        SurveyGrouper([0, 18])


def test_invalid_respondent_age():
    """Проверка обработки недопустимого возраста"""
    grouper = SurveyGrouper([18, 25])
    with pytest.raises(ValueError):
        grouper.add_respondent(Respondent("Иванов Иван Иванович", 124))

    with pytest.raises(ValueError):
        grouper.add_respondent(Respondent("Иванов Иван Иванович", -1))
