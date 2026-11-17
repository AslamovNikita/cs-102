"""Приложение для распределения респондентов по возрастным группам"""
import sys


class Respondent:
    """Участник опроса"""

    def __init__(self, full_name, age):
        """Сохраняет имя и возраст"""
        self.full_name = full_name
        self.age = age


class AgeGroup:
    """Возрастная группа"""

    def __init__(self, lower_bound, upper_bound=None):
        """Создаёт возрастную группу с заданными границами"""
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.respondents = []

    @property
    def label(self):
        """Возвращает обозначение возрастной группы текстом"""
        if self.upper_bound is None:
            return f"{self.lower_bound}+"
        return f"{self.lower_bound}-{self.upper_bound}"

    def contains(self, age):
        """Проверяет входит ли возраст в эту группу"""
        if age < self.lower_bound:
            return False
        if self.upper_bound is None:
            return True
        return age <= self.upper_bound

    def add(self, respondent):
        """Добавляет респондента в групп"""
        self.respondents.append(respondent)

    def format(self):
        """Формирует строку с респондентами группы"""
        if not self.respondents:
            return None
        sorted_respondents = sorted(
            self.respondents,
            key=lambda respondent: (
                -respondent.age,
                respondent.full_name,
            ),
        )
        people = ", ".join(
            f"{respondent.full_name} ({respondent.age})"
            for respondent in sorted_respondents
        )

        return f"{self.label}: {people}"


class SurveyGrouper:
    """Распределяет респондентов по возрастным группам"""

    def __init__(self, boundaries):
        """Создаёт возрастные группы по заданным границам"""
        if not boundaries:
            raise ValueError("Необходимо указать границы возрастных групп.")
        if any(boundary <= 0 for boundary in boundaries):
            raise ValueError("Границы должны быть положительными числами.")
        if boundaries != sorted(set(boundaries)):
            raise ValueError("Границы должны строго возрастать.")
        if boundaries[-1] > 123:
            raise ValueError("Максимальная граница не должна превышать 123.")
        self.groups = []
        lower_bound = 0
        for boundary in boundaries:
            self.groups.append(AgeGroup(lower_bound, boundary))
            lower_bound = boundary + 1

        self.groups.append(AgeGroup(lower_bound))

    def add_respondent(self, respondent):
        """Находит подходящую группу и добавляет в неё"""
        if respondent.age < 0 or respondent.age > 123:
            raise ValueError("Возраст должен быть от 0 до 123 лет.")
        for group in self.groups:
            if group.contains(respondent.age):
                group.add(respondent)
                return

    def get_result(self):
        """Возвращает непустые группы от старшей к младшей"""
        result = []
        for group in reversed(self.groups):
            formatted_group = group.format()
            if formatted_group is not None:
                result.append(formatted_group)
        return result


def read_respondents():
    """Читает респндентов из ввода"""
    respondents = []
    for line in sys.stdin:
        line = line.strip()
        if line == "END":
            break
        if not line:
            continue
        try:
            full_name, age = line.rsplit(",", maxsplit=1)
            full_name = full_name.strip()
            age = int(age.strip())
        except ValueError as error:
            raise ValueError(f"Некорректная строка с респондентом: {line}") from error
        if not full_name:
            raise ValueError("ФИО респондента не может быть пустым.")

        respondents.append(Respondent(full_name, age))
    return respondents


def main():
    """Запуск приложение"""
    try:
        boundaries = [int(value) for value in sys.argv[1:]]
        grouper = SurveyGrouper(boundaries)
        respondents = read_respondents()
        for respondent in respondents:
            grouper.add_respondent(respondent)

        for line in grouper.get_result():
            print(line)
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
