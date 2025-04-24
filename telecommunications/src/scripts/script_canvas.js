const canvas = document.getElementById("miGrafica");
const ctx = canvas.getContext("2d");
const datos = [30, 80, 45, 120, 90]; // Valores para cada barra
const etiquetas = ["A", "B", "C", "D", "E"];
const colores = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD"];

function dibujarGraficoBarras() {
    const margen = 30;
    const anchoBarra = 50;
    const espacio = 20;
  
    // Calcular máximo valor para escalar las barras
    const maxValor = Math.max(...datos);
  
    // Dibujar ejes
    ctx.beginPath();
    ctx.moveTo(margen, margen);
    ctx.lineTo(margen, canvas.height - margen); // Eje Y
    ctx.lineTo(canvas.width - margen, canvas.height - margen); // Eje X
    ctx.strokeStyle = "#333";
    ctx.stroke();
  
    // Dibujar barras
    datos.forEach((valor, i) => {
      const x = margen + espacio + i * (anchoBarra + espacio);
      const altura = ((valor / maxValor) * (canvas.height - 2 * margen)) * 0.8;
      const y = canvas.height - margen - altura;
  
      ctx.fillStyle = colores[i];
      ctx.fillRect(x, y, anchoBarra, altura);
  
      // Etiquetas
      ctx.fillStyle = "#333";
      ctx.fillText(etiquetas[i], x + anchoBarra/4, canvas.height - margen + 20);
    });
}
  
function dibujarGraficoLineas() {
    const puntos = [30, 80, 45, 120, 90];
    ctx.beginPath();
  
    puntos.forEach((valor, i) => {
      const x = margen + i * ((canvas.width - 2 * margen) / (puntos.length - 1));
      const y = canvas.height - margen - (valor / maxValor) * (canvas.height - 2 * margen);
  
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
  
    ctx.strokeStyle = "#FF6B6B";
    ctx.lineWidth = 3;
    ctx.stroke();
}