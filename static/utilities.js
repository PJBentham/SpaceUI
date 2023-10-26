export let statusElement = document.getElementById("status");

export function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
