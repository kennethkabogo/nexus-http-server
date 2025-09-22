import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/Card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/Table";

function RequestLogs() {
  const [logs, setLogs] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await fetch('/api/logs');
      const data = await response.json();
      setLogs(data.logs);
    };

    fetchLogs();

    const interval = setInterval(fetchLogs, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mt-8">
      <Card>
        <CardHeader>
          <CardTitle>Request Logs</CardTitle>
          <CardDescription>A real-time view of the server logs</CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-gray-100 p-4 rounded-md overflow-auto h-96">
            {logs}
          </pre>
        </CardContent>
      </Card>
    </div>
  );
}

export default RequestLogs;