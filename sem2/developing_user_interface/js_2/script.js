// Задание 1: Создание массива
let shoppingList = ["Молоко", "Хлеб", "Яблоки"];
console.log("Длина списка:", shoppingList.length); // 3
shoppingList[1] = "Бананы"; // Замена Хлеба
console.log("Обновленный список:", shoppingList);

// Задание 2: Работа с массивами
let groceryList = [];
groceryList.push("Молоко", "Хлеб", "Яблоки");
groceryList.splice(1, 1, "Бананы", "Апельсины"); // Замена Хлеба
let removedItem = groceryList.pop(); // Удаляем последний элемент (Яблоки)
console.log("Удаленный элемент:", removedItem);
groceryList.sort(); // Сортировка по алфавиту
console.log("Индекс Молоко:", groceryList.indexOf("Молоко"));
groceryList.splice(2, 0, "Морковь", "Огурцы"); // Добавляем после Бананов
let newList = ["Сок", "Попкорн"];
let combinedList = groceryList.concat(newList, newList); // Объединяем дважды
console.log("Последний индекс Попкорн:", combinedList.lastIndexOf("Попкорн"));
console.log("Итоговый список:", combinedList);

// Задание 3: Многомерные массивы
let baseArray = [1, 2, 3];
let nestedArray = [baseArray, baseArray, baseArray];
console.log("Значение 2 из массива:", nestedArray[0][0][1]); // 2

// Задание 4: Работа с объектами
let myCar = {
    make: "Toyota",
    model: "Camry",
    year: 2020
};
let color = "color";
myCar[color] = "синий"; // Динамическое свойство
let forSaleKey = "forSale";
myCar[forSaleKey] = true;
console.log("Марка и модель:", myCar.make, myCar.model);
console.log("Продается?:", myCar[forSaleKey]);

// Задание 5: Объекты и массивы
let people = { friends: [] };
let friend1 = { name: "Иван", surname: "Иванов", id: 1 };
let friend2 = { name: "Петр", surname: "Петров", id: 2 };
let friend3 = { name: "Сергей", surname: "Сергеев", id: 3 };
people.friends.push(friend1, friend2, friend3);
console.log("Список друзей:", people.friends);

// Задание 6: Управление массивом
const theList = ['Laurence', 'Svekis', true, 35, null, undefined, {test: 'one', score: 55}, ['one', 'two']];
theList.shift(); // Удалить первый
theList.pop();   // Удалить последний
theList.unshift("FIRST");
theList.splice(3, 1, "MIDDLE");
theList[3] = "hello World";
theList.push("LAST");
console.log("Результат задания 6:", theList);

// Задание 7: Каталог продукции
let products = [];
let product1 = { name: "Телефон", model: "X1", price: 10000, quantity: 5 };
let product2 = { name: "Ноутбук", model: "Y2", price: 50000, quantity: 3 };
let product3 = { name: "Планшет", model: "Z3", price: 20000, quantity: 8 };
products.push(product1, product2, product3);
console.log("Количество третьего товара:", products[2].quantity);

// Задание 8: Логические операторы
let age = parseInt(prompt("Введите ваш возраст:"));
let message;
if (age >= 21) {
    message = "Разрешить вход в заведение и покупку алкоголя";
} else if (age >= 19) {
    message = "Разрешить вход в заведение и запретить покупку алкоголя";
} else {
    message = "Запретить вход";
}
console.log(message);

// Задание 9: Сочетание операторов
let prize = parseInt(prompt("Выберите число от 0 до 10:"));
let prizeMessage = "My Selection: ";
switch (prize) {
    case 0:
    case 1:
        prizeMessage += "Книга";
        break;
    case 2:
    case 3:
        prizeMessage += "Футболка";
        break;
    case 4:
    case 5:
        prizeMessage += "Чашка";
        break;
    default:
        prizeMessage += "Сертификат";
}
console.log(prizeMessage);

// Задание 12: Камень-ножницы-бумага
let choices = ["Камень", "Ножницы", "Бумага"];
let playerChoice = choices[Math.floor(Math.random() * 3)];
let computerChoice = choices[Math.floor(Math.random() * 3)];
console.log(`Игрок: ${playerChoice}, Компьютер: ${computerChoice}`);

if (playerChoice === computerChoice) {
    console.log("Ничья!");
} else if (
    (playerChoice === "Камень" && computerChoice === "Ножницы") ||
    (playerChoice === "Ножницы" && computerChoice === "Бумага") ||
    (playerChoice === "Бумага" && computerChoice === "Камень")
) {
    console.log("Вы победили!");
} else {
    console.log("Компьютер победил!");
}