const descriptions = ["классный", "замечательный", "ужасный", "веселый"];
function describeName() {
  const name = prompt("Введите ваше имя:");
  const randomIndex = Math.floor(Math.random() * descriptions.length);
  alert(`${name} - ${descriptions[randomIndex]}`);
}
describeName();