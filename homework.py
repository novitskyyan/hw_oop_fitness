from dataclasses import dataclass, astuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_TRAINING_RESULT = ('Тип тренировки: {}; '
                               'Длительность: {:.3f} ч.; '
                               'Дистанция: {:.3f} км; '
                               'Ср. скорость: {:.3f} км/ч; '
                               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Возвращает информацию с данными о тренировке.

        Функция принимает числовые параметры соответствующего типа
        тренировки в виде кортежа со всеми необходимыми данными,
        распаковывает его и подставляет необходимую информацию.
        """
        return self.MESSAGE_TRAINING_RESULT.format(*(astuple(self)))


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
        raise NotImplementedError('Ошибка: не реализован метод '
                                  'в дочернем классе!')

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
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


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
        return ((self.CONST_WEIGHT_WALKING_1 * self.weight
                + (speed_m_sec ** 2
                   / (self.height / self.FROM_CM_IN_M))
                * self.CONST_WEIGHT_WALKING_2 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


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
        return ((self.get_mean_speed()
                + self.CONST_CALORIES_SWIMMING)
                * self.CONST_MULTY_SPEED
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        "SWM": {'class_name': Swimming, 'quantity_args': 5},
        "RUN": {'class_name': Running, 'quantity_args': 3},
        "WLK": {'class_name': SportsWalking, 'quantity_args': 4}
    }
    if workout_type not in training_dict:
        available_trainings = ", ".join(training_dict)
        raise ValueError(f'Введен не предусмотренный тип: {workout_type}. '
                         'Фитнес-трекер обрабатывает '
                         'значения для следующих видов тренировок: '
                         f'{available_trainings}. '
                         'Пожалуйста, удостоверьтесь, что '
                         'выбран один из указанных видов спорта.')
    if len(data) != training_dict[workout_type]['quantity_args']:
        raise ValueError('Отсутствуют все данные, '
                         'необходимые для исчислений.')
    return training_dict[workout_type]['class_name'](*data)


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
