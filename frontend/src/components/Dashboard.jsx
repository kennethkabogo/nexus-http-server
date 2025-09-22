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
import ThreeDBackground from './ThreeDBackground';

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h}h ${m}m ${s}s`;
}

function Dashboard() {
  const [stats, setStats] = useState({ uptime: 0, request_count: 0 });
  const [routes, setRoutes] = useState([]);

  useEffect(() => {
    const fetchRoutes = async () => {
      const response = await fetch('/api/routes');
      const data = await response.json();
      setRoutes(data.routes);
    };

    const fetchStats = async () => {
      const response = await fetch('/api/stats');
      const data = await response.json();
      setStats(data);
    };

    fetchRoutes();
    fetchStats();

    const interval = setInterval(fetchStats, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <ThreeDBackground />
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-4 text-white">Admin Dashboard</h1>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader>
              <CardTitle>Server Status</CardTitle>
              <CardDescription>Current status of the server</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-green-500 font-bold">Running</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Uptime</CardTitle>
              <CardDescription>Server uptime</CardDescription>
            </CardHeader>
            <CardContent>
              <p>{formatUptime(stats.uptime)}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Requests</CardTitle>
              <CardDescription>Total requests handled</CardDescription>
            </CardHeader>
            <CardContent>
              <p>{stats.request_count}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Active Routes</CardTitle>
              <CardDescription>Number of active routes</CardDescription>
            </CardHeader>
            <CardContent>
              <p>{routes.length}</p>
            </CardContent>
          </Card>
        </div>
        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Active Routes</CardTitle>
              <CardDescription>A list of all active routes on the server</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Path</TableHead>
                    <TableHead>Handler</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {routes.map((route) => (
                    <TableRow key={route.path}>
                      <TableCell>{route.path}</TableCell>
                      <TableCell>{route.handler}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

export default Dashboard;