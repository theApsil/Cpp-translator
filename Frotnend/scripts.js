function processData() {
    // Ваш код обработки данных
    var input1Value = document.getElementById('input1').value;

    // Пример обработки: конкатенация данных
    var result = input1Value + ' qwerty';

    // Вывод результата
    document.getElementById('input2').innerHTML = 'Результат: ' + result;
}