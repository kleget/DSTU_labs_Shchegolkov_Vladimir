function calculate(a, b, operator = "+") {
    return operator === "+" ? a + b : a - b;
  }
  
  console.log(calculate(5, 3)); // 8
  console.log(calculate(10, 4, "-")); // 6