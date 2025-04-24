import LightweightChart from './components/charts/LightweightChart.jsx'
import React, { useState, useEffect } from 'react';

function App() {
  const [areaData, setAreaData] = useState([]);
  const [candlestickData, setCandlestickData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = () => {
      const mockAreaData = [
        { time: '2023-01-01', value: 100 },
        { time: '2023-01-02', value: 120 },
        { time: '2023-01-03', value: 90 },
        { time: '2023-01-04', value: 150 },
        { time: '2023-01-05', value: 130 },
        { time: '2023-01-06', value: 160 },
        { time: '2023-01-07', value: 140 },
      ];

      const mockCandlestickData = [
        { time: '2023-01-01', open: 95, high: 110, low: 85, close: 100 },
        { time: '2023-01-02', open: 100, high: 125, low: 95, close: 120 },
        { time: '2023-01-03', open: 120, high: 125, low: 80, close: 90 },
        { time: '2023-01-04', open: 90, high: 160, low: 85, close: 150 },
        { time: '2023-01-05', open: 150, high: 155, low: 120, close: 130 },
        { time: '2023-01-06', open: 130, high: 170, low: 125, close: 160 },
        { time: '2023-01-07', open: 160, high: 165, low: 130, close: 140 },
      ];

      setTimeout(() => {
        setAreaData(mockAreaData);
        setCandlestickData(mockCandlestickData);
        setIsLoading(false);
      }, 1000);
    };

    fetchData();
  }, []);

  return (
    <div className="app-container">
      <h1>Visualización de Datos con Lightweight-Charts</h1>
      
      <div className="chart-container">
        {isLoading ? (
          <div className="loading">Cargando datos...</div>
        ) : (
          <LightweightChart 
            areaData={areaData} 
            candlestickData={candlestickData} 
          />
        )}
      </div>
    </div>
  );
}

export default App;