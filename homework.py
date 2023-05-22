from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки в часах
    distance: float  # дистанция в километрах, которую преодолел пользователь
    speed: float  # средняя скорость
    calories: float  # количество израсходованных калорий

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # остается намеренно, так как логика у каждой тренировки своя

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        calories_from_running = ((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight
                                 / self.M_IN_KM * self.duration
                                 * self.MIN_IN_HOUR)
        return calories_from_running


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    CONST_WEIGHT_WALKING_1: float = 0.035
    CONST_WEIGHT_WALKING_2: float = 0.029
    CONST_FROM_KM_IN_M: float = 0.278
    FROM_CM_IN_M: int = 100

    def get_spent_calories(self) -> float:
        speed_m_sec = self.get_mean_speed() * self.CONST_FROM_KM_IN_M
        calories_from_walking = ((self.CONST_WEIGHT_WALKING_1 * self.weight
                                  + (speed_m_sec ** 2
                                     / (self.height / self.FROM_CM_IN_M))
                                 * self.CONST_WEIGHT_WALKING_2 * self.weight)
                                 * (self.duration * self.MIN_IN_HOUR))
        return calories_from_walking


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int

    LEN_STEP: float = 1.38
    CONST_CALORIES_SWIMMING: float = 1.1
    CONST_MULTY_SPEED: int = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        calories_from_swimming = ((self.get_mean_speed()
                                   + self.CONST_CALORIES_SWIMMING)
                                  * self.CONST_MULTY_SPEED
                                  * self.weight * self.duration)
        return calories_from_swimming


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {"SWM": Swimming,
                     "RUN": Running,
                     "WLK": SportsWalking
                     }
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
