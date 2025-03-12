import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from "@mui/material";

export default function RequestTable() {
  const [data, setData] = useState([
    { url: "https://example.com", safe: true, language: "SQL", bypassable: false },
    { url: "https://test.com", safe: false, language: "SQL", bypassable: true },
    { url: "https://demo.com", safe: true, language: "SQL", bypassable: false },
    { url: "https://secure-site.com", safe: true, language: "SQL", bypassable: true },
    { url: "https://phishing.com", safe: false, language: "SQL", bypassable: false },
  ]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/requests")
      .then((response) => {
        console.log("API Response:", response.data);
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div style={{ width: "100%", padding: "20px", }}>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>Requests Table</h2>
      
      <TableContainer component={Paper} sx={{ width: "100%", boxShadow: 3 }}>
        <Table sx={{ width: "100%" }} aria-label="request table">
          <TableHead sx={{ backgroundColor: "#1976d2" }}>
            <TableRow>
              <TableCell sx={{ color: "white", fontWeight: "bold" }}>URL</TableCell>
              <TableCell align="center" sx={{ color: "white", fontWeight: "bold" }}>Safety</TableCell>
              <TableCell align="center" sx={{ color: "white", fontWeight: "bold" }}>Language</TableCell>
              <TableCell align="center" sx={{ color: "white", fontWeight: "bold" }}>Bypassable</TableCell>
            </TableRow>
          </TableHead>
          
          <TableBody>
            {data.length > 0 ? (
              data.map((entry, index) => (
                <TableRow
                  key={index}
                  sx={{
                    backgroundColor: index % 2 === 0 ? "#f5f5f5" : "white",
                    "&:hover": { backgroundColor: "#e0e0e0" },
                  }}
                >
                  <TableCell>{entry.url}</TableCell>
                  <TableCell align="center">
                    <Chip
                      label={entry.safe ? "Safe" : "Not Safe"}
                      color={entry.safe ? "success" : "error"}
                    />
                  </TableCell>
                  <TableCell align="center">{entry.language}</TableCell>
                  <TableCell align="center">
                    <Chip
                      label={entry.bypassable ? "Yes" : "No"}
                      color={entry.bypassable ? "warning" : "default"}
                    />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  No data available
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
