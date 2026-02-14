import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [logs, setLogs] = useState([]);

  const fetchLogs = async () => {
    try {
      const response = await axios.get("http://localhost:8001/logs");
      setLogs(response.data);
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000); // refresh every 5 sec
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h1>LankaShield AI Monitoring Dashboard</h1>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Voltage</th>
            <th>Load %</th>
            <th>Temperature</th>
            <th>Risk Score</th>
            <th>Status</th>
            <th>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.voltage}</td>
              <td>{log.load_percentage}</td>
              <td>{log.temperature}</td>
              <td>{log.risk_score}</td>
              <td
                style={{
                  color: log.anomaly_detected ? "red" : "green",
                  fontWeight: "bold",
                }}
              >
                {log.anomaly_detected ? "ANOMALY" : "NORMAL"}
              </td>
              <td>{new Date(log.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

<h2>Risk Score Trend</h2>

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={logs}>
    <CartesianGrid stroke="#ccc" />
    <XAxis dataKey="id" />
    <YAxis />
    <Tooltip />
    <Line type="monotone" dataKey="risk_score" stroke="#ff0000" />
  </LineChart>
</ResponsiveContainer>

    </div>
  );
}

export default App;
