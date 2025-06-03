var cols = 12
var rows = 12;
var w; // Cell size
var grid = [];
var current;
var stack = [];

var seed = 513;

function setup() {
  //Good seeds: 126, 513
  //bad seeds 512
    randomSeed(513);

  createCanvas(400, 400);
  w = min(400/cols, 400/rows);

  // Create grid of cells
  for (let j = 0; j < rows; j++) {
    for (let i = 0; i < cols; i++) {
      let cell = new Cell(i, j);
      grid.push(cell);
    }
  }

  current = grid[0];

  var gui = createGui('My awesome GUI');
  gui.addGlobals('seed', 'cols', 'rows');

  //button = createButton("Click me!");
  //button.mousePressed(buttonClicked);

}

function buttonClicked() {
  console.log("Button clicked!");
}


function draw() {
  background(51);

  // Draw all cells
  for (let i = 0; i < grid.length; i++) {
    grid[i].show();
  }

  current.visited = true;
  current.highlight();

  // Step 1: Choose a random neighbor
  let next = current.checkNeighbors();
  if (next) {
    next.visited = true;

    // Step 2: Push current cell to the stack
    stack.push(current);

    // Step 3: Remove the wall between current and next
    removeWalls(current, next);

    // Step 4: Make the chosen cell the current cell
    current = next;
  } else if (stack.length > 0) {
    current = stack.pop();
  }
}

// Helper to get grid index
function index(i, j) {
  if (i < 0 || j < 0 || i >= cols || j >= rows) {
    return -1;
  }
  return i + j * cols;
}

// Cell object
class Cell {
  constructor(i, j) {
    this.i = i;
    this.j = j;
    this.walls = [true, true, true, true]; // Top, right, bottom, left
    this.visited = false;
  }

  show() {
    let x = this.i * w;
    let y = this.j * w;
    stroke(255);
    if (this.walls[0]) line(x, y, x + w, y); // Top
    if (this.walls[1]) line(x + w, y, x + w, y + w); // Right
    if (this.walls[2]) line(x + w, y + w, x, y + w); // Bottom
    if (this.walls[3]) line(x, y + w, x, y); // Left

    if (this.visited) {
      noStroke();
      fill(255, 0, 255, 100);
      rect(x, y, w, w);
    }
  }

  highlight() {
    let x = this.i * w;
    let y = this.j * w;
    noStroke();
    fill(0, 255, 0, 150);
    rect(x, y, w, w);
  }

  checkNeighbors() {
    let neighbors = [];

    let top = grid[index(this.i, this.j - 1)];
    let right = grid[index(this.i + 1, this.j)];
    let bottom = grid[index(this.i, this.j + 1)];
    let left = grid[index(this.i - 1, this.j)];

    if (top && !top.visited) neighbors.push(top);
    if (right && !right.visited) neighbors.push(right);
    if (bottom && !bottom.visited) neighbors.push(bottom);
    if (left && !left.visited) neighbors.push(left);

    if (neighbors.length > 0) {
      let r = floor(random(0, neighbors.length));
      return neighbors[r];
    } else {
      return undefined;
    }
  }
}

// Remove walls between two cells
function removeWalls(a, b) {
  let x = a.i - b.i;
  if (x === 1) {
    a.walls[3] = false;
    b.walls[1] = false;
  } else if (x === -1) {
    a.walls[1] = false;
    b.walls[3] = false;
  }

  let y = a.j - b.j;
  if (y === 1) {
    a.walls[0] = false;
    b.walls[2] = false;
  } else if (y === -1) {
    a.walls[2] = false;
    b.walls[0] = false;
  }
}

function download(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}
