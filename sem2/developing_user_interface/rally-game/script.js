document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;

    // Игровые объекты
    const car = { 
        x: canvas.width / 2 - 25, 
        y: canvas.height - 120, 
        width: 50, 
        height: 100,
        speed: 5
    };
    
    let obstacles = [];
    let keys = {};
    let score = 0;
    let gameRunning = false;
    let obstacleInterval;
    let speedInterval;
    let currentSpeed = 2;

    // Изображения
    const carImage = new Image();
    carImage.src = 'assets/car.png';

    const obstacleImage = new Image();
    obstacleImage.src = 'assets/obstacle.png';

    // Рекорды
    let records = getRecords();

    // Обработчики клавиатуры
    document.addEventListener('keydown', (e) => {
        keys[e.key] = true;
    });

    document.addEventListener('keyup', (e) => {
        keys[e.key] = false;
    });

    // Игровые функции
    function startGame() {
        car.x = canvas.width / 2 - 25;
        car.y = canvas.height - 120;
        score = 0;
        obstacles = [];
        currentSpeed = 2;
        document.getElementById('score').textContent = 'Счет: 0';
        
        // Генерация препятствий
        obstacleInterval = setInterval(generateObstacle, 1000);
        
        // Увеличение сложности
        speedInterval = setInterval(() => {
            currentSpeed += 0.5;
        }, 5000);
        
        gameRunning = true;
        requestAnimationFrame(gameLoop);
    }

    function gameLoop() {
        if (!gameRunning) return;
        
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    function update() {
        // Движение машины
        if (keys['ArrowLeft'] || keys['a']) {
            car.x -= car.speed;
        }
        if (keys['ArrowRight'] || keys['d']) {
            car.x += car.speed;
        }
        car.x = Math.max(0, Math.min(canvas.width - car.width, car.x));

        // Движение препятствий
        for (const obs of obstacles) {
            obs.y += currentSpeed;
        }
        
        // Удаление вышедших за экран препятствий
        obstacles = obstacles.filter(obs => obs.y < canvas.height);
        
        // Проверка столкновений
        for (const obs of obstacles) {
            if (checkCollision(car, obs)) {
                gameOver();
                return;
            }
        }
        
        score++;
        document.getElementById('score').textContent = `Счет: ${score}`;
    }

    function draw() {
        // Очистка экрана
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Рисование дороги (фон)
        ctx.fillStyle = '#888';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Рисование машины
        ctx.drawImage(carImage, car.x, car.y, car.width, car.height);
        
        // Рисование препятствий
        for (const obs of obstacles) {
            ctx.drawImage(obstacleImage, obs.x, obs.y, obs.width, obs.height);
        }
    }

    function generateObstacle() {
        const width = 50;
        const height = 100;
        const x = Math.random() * (canvas.width - width);
        obstacles.push({ 
            x, 
            y: -height, 
            width, 
            height 
        });
    }

    function checkCollision(a, b) {
        return a.x < b.x + b.width &&
               a.x + a.width > b.x &&
               a.y < b.y + b.height &&
               a.y + a.height > b.y;
    }

    function gameOver() {
        gameRunning = false;
        clearInterval(obstacleInterval);
        clearInterval(speedInterval);
        
        // Проверка на рекорд
        if (score > (records[records.length-1]?.score || 0)) {
            document.getElementById('recordModal').classList.remove('hidden');
        } else {
            alert(`Игра окончена! Ваш счет: ${score}`);
        }
    }

    // Рекорды
    function getRecords() {
        const cookie = document.cookie.split('; ')
            .find(row => row.startsWith('records='));
        
        if (cookie) {
            try {
                return JSON.parse(decodeURIComponent(cookie.split('=')[1]));
            } catch (e) {
                return Array(10).fill({ name: 'AAA', score: 0 });
            }
        }
        
        return Array(10).fill({ name: 'AAA', score: 0 });
    }

    function saveRecords(newRecords) {
        document.cookie = `records=${encodeURIComponent(JSON.stringify(newRecords))}; path=/`;
    }

    function addRecord(name, score) {
        records.push({ name, score });
        records.sort((a, b) => b.score - a.score);
        records = records.slice(0, 10);
        saveRecords(records);
        showRecords();
    }

    function showRecords() {
        const ul = document.getElementById('recordsList');
        ul.innerHTML = '';
        
        records.forEach((record, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. ${record.name} - ${record.score}`;
            ul.appendChild(li);
        });
        
        document.getElementById('recordsTable').classList.remove('hidden');
    }

    // Обработчики событий
    document.getElementById('newGame').addEventListener('click', startGame);
    document.getElementById('records').addEventListener('click', showRecords);
    
    document.getElementById('closeRecords').addEventListener('click', () => {
        document.getElementById('recordsTable').classList.add('hidden');
    });
    
    document.getElementById('saveRecord').addEventListener('click', () => {
        const name = document.getElementById('playerName').value.trim();
        if (name) {
            addRecord(name, score);
            document.getElementById('recordModal').classList.add('hidden');
            document.getElementById('playerName').value = '';
        }
    });

    // Инициализация игры после загрузки изображений
    function init() {
        if (carImage.complete && obstacleImage.complete) {
            startGame();
        } else {
            requestAnimationFrame(init);
        }
    }

    carImage.onload = obstacleImage.onload = init;
});