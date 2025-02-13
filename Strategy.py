from abc import ABC, abstractmethod

class ActionStrategy(ABC):
    @abstractmethod
    def execute(self, student):
        pass

class Student:
    def __init__(self, name, surname, hp, sanity, excitement, iq, energy):
        self.name = name
        self.surname = surname
        self.hp = hp  # очки здоровья персонажа
        self.sanity = sanity
        self.excitement = excitement
        self.iq = iq
        self.energy = energy

    def start_game(self):
        self.name, self.surname = input().split()
        self.hp = 100
        self.sanity = 100
        self.excitement = 50
        self.iq = 20
        self.energy = 100

    def is_alive(self):
        return self.hp > 0

    def show(self):
        if self.is_alive():
            print(
                f"{self.name} {self.surname}: HP = {str(self.hp).zfill(3)}, Energy = {str(self.energy).zfill(3)}, IQ = {str(self.iq).zfill(3)}, Sanity = {str(self.sanity).zfill(3)}, Excitement = {str(self.excitement).zfill(3)}.")
        else:
            print(
                f"{self.name} {self.surname}: HP = {str(self.hp).zfill(3)}, Energy = {str(self.energy).zfill(3)}, IQ = {str(self.iq).zfill(3)}, Sanity = {str(self.sanity).zfill(3)}, Excitement = {str(self.excitement).zfill(3)}. Game over.")

    def perform_action(self, strategy: ActionStrategy):
        strategy.execute(self)

class EatStrategy(ActionStrategy):
    def execute(self, student):
        if student.is_alive():
            student.hp = min(student.hp + 1, 100)
            student.energy = min(student.energy + 7, 100)
            student.iq = max(student.iq - 1, 0)
            student.excitement = max(student.excitement - 2, 0)
class WaitStrategy(ActionStrategy):
    def execute(self, student):
        if student.is_alive():
            student.hp = min(student.hp + 1, 100)
            student.energy = max(student.energy - 3, 0)
            student.excitement = max(student.excitement - 3, 0)

class StudyStrategy(ActionStrategy):
    def execute(self, student):
        if student.is_alive():
            student.hp = max(student.hp - 2, 0)
            student.energy = max(student.energy - 4, 0)
            student.iq = min(student.iq + 5, 100)
            student.sanity = max(student.sanity - 5, 0)
            student.excitement = max(student.excitement - 2, 0)

class SleepStrategy(ActionStrategy):
    def execute(self, student):
        if student.is_alive():
            student.hp = min(student.hp + 2, 100)
            student.energy = max(student.energy - 2, 0)
            student.sanity = min(student.sanity + 7, 100)

class Watch_tvStrategy(ActionStrategy):
    def execute(self, student):
        if student.is_alive():
            student.hp = max(student.hp - 2, 0)
            student.energy = max(student.energy - 3, 0)
            student.iq = max(student.iq - 3, 0)
            student.sanity = min(student.sanity + 1, 100)
            student.excitement = min(student.excitement + 5, 100)


def main():
    student = Student("", "", 0, 0, 0, 0 , 0)
    student.start_game()
    moves = int(input())
    actions = {
        "Wait": WaitStrategy(),
        "Eat": EatStrategy(),
        "Study": StudyStrategy(),
        "Sleep": SleepStrategy(),
        "Watch TV": Watch_tvStrategy()
    }
    for i in range(moves):
        move = str(input())
        student.perform_action(actions[move])
        student.show()


if __name__ == "__main__":
    main()