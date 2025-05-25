const ConfidenceBar = ({ confidence }) => {
  const percentage = Math.min(100, Math.max(0, Math.round(confidence * 100)));
  return (
    <div className="confidence-section">
      <h3>Confidence Level {percentage >= 70 ? '💪' : percentage >= 50 ? '👍' : '🤔'}</h3>
      <div className="confidence-bar-container">
        <div 
          className="confidence-bar-fill"
          style={{ width: `${percentage}%` }}
        />
        <span className="confidence-text">{percentage}%</span>
      </div>
    </div>
  );
};
export default ConfidenceBar;