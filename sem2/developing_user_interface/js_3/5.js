const multiplicationTable = [];
const size = 10;

for (let i = 0; i <= size; i++) {
  const temp = [];
  for (let j = 0; j <= size; j++) {
    temp.push(i * j);
  }
  multiplicationTable.push(temp);
}
console.log(multiplicationTable);