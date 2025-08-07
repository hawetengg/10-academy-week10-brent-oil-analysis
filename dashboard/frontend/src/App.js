import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ReferenceLine } from 'recharts';
import axios from 'axios';
import './App.css';

function App() {
const [priceData, setPriceData] = useState([]);
const [events, setEvents] = useState([]);
const [changePoints, setChangePoints] = useState([]);

useEffect(() => {
    axios.get('http://localhost:5000/api/prices')
    .then(res => {
        const data = res.data.dates.map((date, i) => ({
        date,
        price: res.data.prices[i]
        }));
        setPriceData(data);
    });
    axios.get('http://localhost:5000/api/events')
    .then(res => setEvents(res.data));
    axios.get('http://localhost:5000/api/change_points')
    .then(res => setChangePoints(res.data));
}, []);

return (
    <div style={{ padding: '20px' }}>
    <h1>Brent Oil Price Analysis</h1>
    <LineChart width={800} height={400} data={priceData}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="price" stroke="#8884d8" />
        {changePoints.map(cp => (
        <ReferenceLine key={cp.date} x={cp.date} stroke="red" label={cp.description} />
        ))}
    </LineChart>
    <h2>Key Events</h2>
    <ul>
        {events.map(event => (
        <li key={event.Date}>{event.Date}: {event.Event} - {event.Description}</li>
        ))}
    </ul>
    </div>
);
}

export default App;