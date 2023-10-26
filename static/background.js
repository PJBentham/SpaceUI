export function startStarfield() {
  let stars = [];
  let engineSpeed = 0;

  function setup() {
    let cnv = createCanvas(windowWidth, windowHeight);
    cnv.style('position', 'fixed');
    cnv.style('top', '0');
    cnv.style('left', '0');
    cnv.style('z-index', '-1');
    for (let i = 0; i < 100; i++) {
      stars.push(new Star());
    }

    let enginePowerElem = document.getElementById("enginePower");
    enginePowerElem.addEventListener('input', function() {
      engineSpeed = parseFloat(enginePowerElem.value);
    });
  }

  function draw() {
    background(0);
    translate(width / 2, height / 2);

    for (let star of stars) {
      star.update();
      star.show();
    }
  }

  // Star class
  class Star {
    constructor() {
      this.x = random(-width, width);
      this.y = random(-height, height);
      this.z = random(width);
      this.pz = this.z;
    }

    update() {
      if (engineSpeed === 0) {
        return; // Exit the update function early if engineSpeed is zero.
      }

      this.pz = this.z;
      this.z -= 4 + engineSpeed * 0.5;
      if (this.z < 1) {
        this.z = width;
        this.x = random(-width, width);
        this.y = random(-height, height);
        this.pz = this.z;
      }
    }

    show() {
      fill(255);
      noStroke();
      let sx = map(this.x / this.z, 0, 1, 0, width);
      let sy = map(this.y / this.z, 0, 1, 0, height);
      let px = map(this.x / this.pz, 0, 1, 0, width);
      let py = map(this.y / this.pz, 0, 1, 0, height);

      stroke(255);
      line(px, py, sx, sy);
    }
  }
  // End Starfield

  // Start the P5 sketch
  new p5();
}
