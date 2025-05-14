const myWork = [];
for (let i = 1; i <= 10; i++) {
  const status = i % 2 === 0 ? true : false; // Четные уроки активны
  const lesson = {
    name: `Lesson ${i}`,
    status: status
  };
  myWork.push(lesson);
}
console.log(myWork);