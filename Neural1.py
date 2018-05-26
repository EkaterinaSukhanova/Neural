import numpy as np # для работы с матрицами
import sys # для печати на экран
from read_all_images import read_images
from read_image import read_one_image


class Neural:
    def __init__(self, learning_rate=0.1, arrays_weights_0_1=None, arrays_weights_1_2=None):
        if arrays_weights_0_1 is None:
            arrays_weights_0_1 = np.random.normal(0.0, 2 ** -0.5, (2, 576))
        if arrays_weights_1_2 is None:
            arrays_weights_1_2 = np.random.normal(0.0, 1, (1, 2))
        self.weights_0_1 = arrays_weights_0_1
        self.weights_1_2 = arrays_weights_1_2
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
    return result_list


#тестируем
def detect_object(network: Neural, filename: str):
    input_image = read_one_image(filename)
    answer = network.predict(input_image)

    if answer >= 0.5:
        result_str = "Круг"
        return result_str
    else:
        result_str = "Треугольник"
        return result_str


def training(network: Neural, train: [], epochs: int):
    for i in range(epochs):  # i = 0...3999
        inputs_ = []
        correct_predictions = []
        # проходим по всем значениям
        for inputs_stat, correct_predict in train:
            network.train(np.array(inputs_stat), correct_predict)  # передаем входные данные и ожидаемые
            # сохраняем результаты для подсчета MSE
            inputs_.append(np.array(inputs_stat))
            correct_predictions.append(np.array(correct_predict))

        train_loss = MSE(network.predict(np.array(inputs_).T), np.array(correct_predictions))
        # sys.stdout.write(
        #     "\rProgress: {}, Training loss: {}".format(str(100 * i / float(epochs))[:4], str(train_loss)[:5]))
        process = "\rProgress: {}, Training loss: {}".format(str(100 * i / float(epochs))[:4], str(train_loss)[:5])


def read_weight():
    arrays_weights_0_1 = []
    with open('weights_0_1.txt', 'r') as f:
        arr = []
        for line in f:
            if line == ';\n':
                arrays_weights_0_1.append(arr)
                arr = []
            else:
                arr.append(float(line))
        if len(arr) > 0:
            arrays_weights_0_1.append(arr)
    arrays_weights_0_1 = np.array(arrays_weights_0_1)

    arrays_weights_1_2 = []
    with open('weights_1_2.txt', 'r') as f:
        arr = []
        for line in f:
            if line == ';\n':
                arrays_weights_1_2.append(arr)
                arr = []
            else:
                arr.append(float(line))
        if len(arr) > 0:
            arrays_weights_1_2.append(arr)
    arrays_weights_1_2 = np.array(arrays_weights_1_2)
    return arrays_weights_0_1, arrays_weights_1_2


def result_in_number(network: Neural, train: []):
    for inputs_stat, correct_predict in train:
        print("the prediction: {}, expected: {}".format(
            str(network.predict(np.array(inputs_stat)) > 0.5),
            str(correct_predict == 1)))

    for inputs_stat, correct_predict in train:
        print("the prediction: {}, expected: {}".format(
            str(network.predict(np.array(inputs_stat))),
            str(correct_predict == 1)))

def write_weights_in_file(network: Neural):
    with open('weights_0_1.txt', 'w') as f:
        for arr in network.weights_0_1:
            for item in arr:
                f.write(str(item) + "\n")
            f.write(";" + "\n")
    with open('weights_1_2.txt', 'w') as f:
        for arr in network.weights_1_2:
            for item in arr:
                f.write(str(item) + "\n")
            f.write(";" + "\n")

def start_training():
    circles = read_images("circle", 1)
    triangle = read_images("triangle", 0)
    train = get_one_list(circles, triangle)
    arrays_weights_0_1, arrays_weights_1_2 = read_weight()

    epochs = 5000
    # насколько быстро за каждую иттерацию нужно сдвигаться
    learning_rate = 0.04

    network = Neural(learning_rate=learning_rate, arrays_weights_0_1=arrays_weights_0_1, arrays_weights_1_2=arrays_weights_1_2)
    training(network=network, train=train, epochs=epochs)
    return network

def start_detect(network: Neural, filename: str):
    return detect_object(network, filename)


if __name__ == "__main__":
    network = start_training()

    filename = "image_test/triangle10.png"
    result = start_detect(network, filename)
    print(result)


