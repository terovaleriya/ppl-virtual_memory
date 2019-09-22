from abc import ABC, abstractmethod
from typing import List, Union


class Animal(ABC):
    def __init__(self, name: str):
        self.name = name

    def happy_behaviour(self):
        self.happy_movement()
        self.scream()

    @abstractmethod
    def happy_movement(self):
        pass

    @abstractmethod
    def greeting(self):
        pass

    @abstractmethod
    def scream(self):
        pass


class Dog(Animal):
    def __init__(self, name: str):
        super().__init__(name)
        pass

    def greeting(self):
        print("Р-р-р-р, меня зовут " + self.name)

    def happy_movement(self):
        print("Виляю хвостом")

    def scream(self):
        print("Гавкаю")


class Cat(Animal):
    def greeting(self):
        print("Мур-р-р, мяу, " + self.name + " мое имя")

    def __init__(self, name: str):
        super().__init__(name)

    def happy_movement(self):
        print("Трусь о ногу")

    def scream(self):
        print("Мяукаю")


if __name__ == '__main__':
    animals: List[Animal] = [Dog("Шарик"), Cat("Мурка")]
    for animal in animals:
        animal.greeting()
    for animal in animals:
        animal.happy_behaviour()
