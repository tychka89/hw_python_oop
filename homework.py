from dataclasses import asdict, dataclass
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    CONST_INFO = ('Тип тренировки: {training_type}; '
                  'Длительность: {duration:.3f} ч.; '
                  'Дистанция: {distance:.3f} км; '
                  'Ср. скорость: {speed:.3f} км/ч; '
                  'Потрачено ккал: {calories:.3f}.'
                  )

    def get_message(self):
        return self.CONST_INFO.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_in_hours: float = duration
        self.weight_in_kilo: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration_in_hours
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Реализуется в дочерних классах.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_in_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                          - self.coeff_calorie_2) * self.weight_in_kilo
                          / self.M_IN_KM * self.duration_in_hours
                          * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_in_ms: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.coeff_calorie_3 * self.weight_in_kilo
                                 + (self.get_mean_speed() ** 2
                                  // self.height_in_ms)
                                 * self.coeff_calorie_4 * self.weight_in_kilo)
                                 * self.duration_in_hours * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 count_pool: int,
                 length_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_in_meters: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool_in_meters * self.count_pool
                             / self.M_IN_KM / self.duration_in_hours)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.get_mean_speed() + self.coeff_calorie_5)
                                 * self.coeff_calorie_6 * self.weight_in_kilo)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    """if workout_type in training_dict.keys():
        return training_dict[workout_type](*data)
    raise BaseException(f'Тренировка {workout_type} не реализована')"""

    if workout_type not in training_dict:
        raise BaseException(f'Тренировка {workout_type} не реализована')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: None = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
