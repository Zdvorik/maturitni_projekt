// Smaže všechny classy s názvem alert po 5 vteřinách
setTimeout(function() {
  document.querySelectorAll('.alert').forEach(function(alert) {
    alert.remove();
  });
}, 5000);


// Proměnné pro samopohybujícího se hada
let x = Math.floor(window.innerWidth / 2 / 20) * 20;
let y = 50;

let speed = 1;
let direction = "right";
const directions = ["up", "down", "left", "right"];
let snake = [{ x, y }];
const maxSize = 5;

// Vytvoření kontejneru pro hada
const snakeContainer = document.createElement("div");
document.body.appendChild(snakeContainer);

// Vykreslení hada
function drawSnake() {
    snakeContainer.innerHTML = "";

    snake.forEach(segment => {
        const div = document.createElement("div");
        div.classList.add("snake-segment");
        div.style.left = segment.x + "px";
        div.style.top = segment.y + "px";
        snakeContainer.appendChild(div);
    });
}

// Pohyb hada
function moveSnake() {
    let newHead = { ...snake[0] };

    // Na základě směru měníme pozici hlavy hada
    switch (direction) {
        case "up": newHead.y -= speed; break;
        case "down": newHead.y += speed; break;
        case "left": newHead.x -= speed; break;
        case "right": newHead.x += speed; break;
    }

    // Zabránění pohybu mimo hranice obrazovky
    if (newHead.x < 0) direction = "right";
    if (newHead.x + 20 > window.innerWidth) direction = "left";
    if (newHead.y < 0) direction = "down";
    if (newHead.y + 20 > window.innerHeight) direction = "up";

    snake.unshift(newHead); 
    if (snake.length > maxSize) snake.pop(); 

    drawSnake();
    requestAnimationFrame(moveSnake);
}

// Změna směru hada (náhodně bez otočení zpět)
function changeDirection() {
    let newDirection;
    do {
        newDirection = directions[Math.floor(Math.random() * directions.length)];
    } while (
        (direction === "up" && newDirection === "down") ||
        (direction === "down" && newDirection === "up") ||
        (direction === "left" && newDirection === "right") ||
        (direction === "right" && newDirection === "left")
    );

    direction = newDirection; // Nastavení nového směru
}

// Spuštění hry
drawSnake(); // Zobrazíme hada
moveSnake(); // Spustíme pohyb hada
setInterval(changeDirection, 1500); // Změna směru každých 1.5 sekundy
