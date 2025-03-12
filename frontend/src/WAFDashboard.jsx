import { useEffect, useState } from "react";
import axios from "axios";

export default function WAFDashboard() {
  const [logs, setLogs] = useState([]);
  const [rules, setRules] = useState([]);

  useEffect(() => {
    fetchLogs();
    fetchRules();
  }, []);

  const fetchLogs = async () => {
    try {
      const response = await axios.get("http://localhost:5000/logs");
      setLogs(response.data);
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };

  const fetchRules = async () => {
    try {
      const response = await axios.get("http://localhost:5000/rules");
      setRules(response.data);
    } catch (error) {
      console.error("Error fetching rules:", error);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">WAF Dashboard</h1>

      {/* Blocked Requests Table */}
      <div className="bg-white p-4 shadow-md rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-3">Blocked Requests</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">IP Address</th>
                <th className="border p-2">Reason</th>
                <th className="border p-2">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {logs.length > 0 ? (
                logs.map((log, index) => (
                  <tr key={index} className="text-center">
                    <td className="border p-2">{log.ip}</td>
                    <td className="border p-2">{log.reason}</td>
                    <td className="border p-2">{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" className="border p-2 text-center text-gray-500">
                    No logs available
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Security Rules */}
      <div className="bg-white p-4 shadow-md rounded-lg">
        <h2 className="text-xl font-semibold mb-3">Security Rules</h2>
        <ul className="list-disc list-inside">
          {rules.length > 0 ? (
            rules.map((rule, index) => (
              <li key={index} className="mb-2">{rule.description}</li>
            ))
          ) : (
            <p className="text-gray-500">No security rules available</p>
          )}
        </ul>
        <button className="bg-blue-500 text-white px-4 py-2 rounded mt-4 hover:bg-blue-600 transition">
          Add New Rule
        </button>
      </div>
    </div>
  );
}
