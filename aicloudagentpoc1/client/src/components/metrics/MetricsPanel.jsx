// components/metrics/MetricsPanel.jsx
export default function MetricsPanel({ projectId }) {
  const metrics = null; // fetch later

  if (!metrics) {
    return <p>No metrics yet</p>;
  }

  return (
    <div>
      <h3>Metrics</h3>
      {/* CPU, memory, cost, uptime */}
    </div>
  );
}
