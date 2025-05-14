const showOne = () => console.log("one");
const showTwo = () => console.log("two");
const showThree = () => {
  console.log("three");
  showOne();
  showTwo();
};

const showFour = () => {
  console.log("four");
  setTimeout(showOne, 0);
  setTimeout(showThree, 0);
};
showFour();