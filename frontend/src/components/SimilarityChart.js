import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

const SimilarityChart = ({ similarity }) => {
  const simValue =
    typeof similarity === 'number' && !isNaN(similarity)
      ? similarity
      : 0.5;

  const data = {
    labels: ['Similar ✅', 'Different 🚫'],
    datasets: [
      {
        data: [simValue * 100, (1 - simValue) * 100],
        backgroundColor: ['rgba(46, 204, 113, 0.9)', 'rgba(246, 43, 87, 0.9)'],
        borderColor: ['rgba(46, 204, 113, 1)', 'rgb(254, 60, 102)'],
        borderWidth: 1
      }
    ]
  };

  const options = {
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: 'Similarity Analysis'
      }
    }
  };

  return (
    <div className="similarity-section">
      <h3>Similarity Analysis</h3>
      <div className="chart-container">
        <Pie data={data} options={options} />
      </div>
    </div>
  );
};

export default SimilarityChart;