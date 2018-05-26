import numpy as np # для работы с матрицами
import sys # для печати на экран
from read_all_images import read_images
from read_image import read_one_image


class Neural:
    def __init__(self, learning_rate = 0.1, arrays = np.random.normal(0.0, 2 ** -0.5, (2, 576))):    #конструктор, learning_rate - скорость обучения стоит по умолчанию, но его можно менять
        self.weights_0_1 = arrays #np.random.normal(0.0, 2 ** -0.5, (2, 576)) #задаем рандомные значения от 0 уровня к 1. На входе 10 нейронов, идут к 2
        self.weights_1_2 = np.random.normal(0.0, 1, (1, 2))
        self.sigmoid_mapper = np.vectorize(self.sigmoid)# позволяет пробежаться по вектору, к каждому элементу применить сигмоидную функцию и оставить результат
        self.learning_rate = np.array([learning_rate]) #список передали в метод, который сделает массив из списка

    def sigmoid(self, x):   #сигмоид
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs): #прямое распространение (предсказание) (слева направа). в inputs передаем 1 и 0. должен иметь размер = количеству входных нейронов
        inputs_1 = np.dot(self.weights_0_1, inputs)#умножаем веса от входного уровня умножаем на inputs
        outputs_1 = self.sigmoid_mapper(inputs_1)#прогоняем их все через сигмоид

        inputs_2 = np.dot(self.weights_1_2, outputs_1)
        outputs_2 = self.sigmoid_mapper(inputs_2)
        return outputs_2 #одно число получаем

    def train(self, inputs: np.array, expected_predict: int):
        inputs_1 = np.dot(self.weights_0_1, inputs)
        outputs_1 = self.sigmoid_mapper(inputs_1)

        inputs_2 = np.dot(self.weights_1_2, outputs_1)
        outputs_2 = self.sigmoid_mapper(inputs_2)
        actual_predict = outputs_2[0]

        error_layer_2 = np.array([actual_predict - expected_predict]) #ошибка
        gradient_layer_2 = actual_predict * (1 - actual_predict) #это дифференцал по dx
        weights_delta_layer_2 = error_layer_2 * gradient_layer_2 #дельта весов
        self.weights_1_2 -= (np.dot(weights_delta_layer_2, outputs_1.reshape(1, len(outputs_1)))) * self.learning_rate #изменение весов от 2 уровня к последнему

        #тоже самое для скрытого уровня
        error_layer_1 = weights_delta_layer_2 * self.weights_1_2
        gradient_layer_1 = outputs_1 * (1 - outputs_1)
        weights_delta_layer_1 = error_layer_1 * gradient_layer_1
        self.weights_0_1 -= np.dot(inputs.reshape(len(inputs), 1), weights_delta_layer_1).T * self.learning_rate


#метод, кот. оценивает кач-во по ср.кв.откл.
def MSE(pred, real):
    return np.mean((pred - real) ** 2)


def get_one_list(first: [], second: []) -> []:
    result_list = list() #[]
    for q in range(0, len(first)):
        result_list.append(first[q])
        result_list.append(second[q])
    # for w in range(0, len(second)):
    #     result_list.append(second[w])
    return result_list


circles = read_images("circle", 1)
triangle = read_images("triangle", 0)
train = get_one_list(circles, triangle)

# train = [
#     ([0, 0, 0], 0),
#     ([0, 0, 1], 1),
#     ([0, 1, 0], 0),
#     ([0, 1, 1], 0),
#     ([1, 0, 0], 1),
#     ([1, 0, 1], 1),
#     ([1, 1, 0], 0),
#     ([1, 1, 1], 1)
# ]

#сколько раз прогоним кейсы
epochs = 5000
#насколько быстро за каждую иттерацию нужно сдвигаться
learning_rate = 0.04

arrays = []
with open('weights.txt', 'r') as f:
    arr = []
    for line in f:
        if line == ';\n':
            arrays.append(arr)
            arr.clear()
        else:
            arr.append(float(line))
    if len(arr) > 0:
        arrays.append(arr)

network = Neural(learning_rate=learning_rate, arrays=arrays)

#запись весов в файл
# with open('weights.txt', 'w') as f:
#     for arr in network.weights_0_1:
#         for item in arr:
#             f.write(str(item) + "\n")
#         f.write(";" + "\n")

for i in range(epochs): # i = 0...3999
    inputs_ = []
    correct_predictions = []
    #проходим по всем значениям
    for inputs_stat, correct_predict in train:
        network.train(np.array(inputs_stat), correct_predict) #передаем входные данные и ожидаемые
        #сохраняем результаты для подсчета MSE
        inputs_.append(np.array(inputs_stat))
        correct_predictions.append(np.array(correct_predict))

    train_loss = MSE(network.predict(np.array(inputs_).T), np.array(correct_predictions))
    sys.stdout.write("\rProgress: {}, Training loss: {}".format(str(100 * i / float(epochs))[:4], str(train_loss)[:5]))

# for inputs_stat, correct_predict in train:
#     print("the prediction: {}, expected: {}".format(
#         str(network.predict(np.array(inputs_stat)) > 0.5),
#         str(correct_predict == 1)))
#
# for inputs_stat, correct_predict in train:
#     print("the prediction: {}, expected: {}".format(
#         str(network.predict(np.array(inputs_stat))),
#         str(correct_predict == 1)))

#тестируем
test = read_one_image("triangle10")
answer = network.predict(test)

if answer >= 0.5:
    print("Круг")
else:
    print("Треугольник")
