function countToTen(num) {
    console.log(num);
    if (num >= 10) return;
    countToTen(num + 1);
  }
  countToTen(5); // 5,6,7,8,9,10