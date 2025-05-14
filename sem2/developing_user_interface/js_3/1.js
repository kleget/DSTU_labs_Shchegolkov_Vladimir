// Генерация случайного числа от 1 до 5
const maxNumber = 5;
const randomNumber = Math.floor(Math.random() * maxNumber) + 1;
let isGuessed = false;

// Цикл запроса числа от пользователя
while (!isGuessed) {
  const userGuess = parseInt(prompt("Угадай число от 1 до 5:"));
  
  if (userGuess === randomNumber) {
    alert("Поздравляем! Вы угадали!");
    isGuessed = true;
  } else {
    alert("Попробуйте ещё раз.");
  }
}