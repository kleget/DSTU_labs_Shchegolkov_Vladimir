function countdown(start) {
    console.log(start);
    if (start < 1) return;
    countdown(start - 1);
  }
  countdown(10);