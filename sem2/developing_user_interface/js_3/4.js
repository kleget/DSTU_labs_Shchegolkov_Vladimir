const grid = [];
let row = [];
const cells = 64;

for (let i = 1; i <= cells; i++) {
  row.push(i);
  if (i % 8 === 0) {
    grid.push(row);
    row = [];
  }
}
console.log(grid);