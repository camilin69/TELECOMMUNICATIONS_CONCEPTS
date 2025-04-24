import React, { useEffect, useRef } from 'react';
import { createChart, AreaSeries, CandlestickSeries } from 'lightweight-charts';

const LightweightChart = ({ areaData, candlestickData }) => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    // Configuración inicial del gráfico
    const chartOptions = { 
      layout: { 
        textColor: 'black', 
        background: { type: 'solid', color: 'white' } 
      } 
    };
    
    const chart = createChart(chartContainerRef.current, chartOptions);
    chartRef.current = chart;

    // Crear series
    const areaSeries = chart.addSeries(AreaSeries, {
      lineColor: '#2962FF', 
      topColor: '#2962FF',
      bottomColor: 'rgba(41, 98, 255, 0.28)',
    });

    const candlestickSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#26a69a', 
      downColor: '#ef5350', 
      borderVisible: false,
      wickUpColor: '#26a69a', 
      wickDownColor: '#ef5350',
    });

    // Establecer datos si están disponibles
    if (areaData && areaData.length > 0) {
      areaSeries.setData(areaData);
    }

    if (candlestickData && candlestickData.length > 0) {
      candlestickSeries.setData(candlestickData);
    }

    chart.timeScale().fitContent();

    // Función de limpieza
    return () => {
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, []);


  return <div ref={chartContainerRef} style={{ width: '100%', height: '400px' }} />;
};

export default LightweightChart;