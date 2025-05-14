const results = [];
function calculate(a, b) {
  return a + b;
}

for (let i = 0; i < 10; i++) {
  const num1 = i * 5;
  const num2 = i * i;
  results.push(calculate(num1, num2));
}
console.log(results); // [0, 6, 14, 24, 36, 50, 66, 84, 104, 126]