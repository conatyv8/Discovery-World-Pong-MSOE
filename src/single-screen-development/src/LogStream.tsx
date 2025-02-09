import { Box } from '@mui/material';
import { useEffect, useState } from 'react';

function LogStream() {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        const eventSource = new EventSource('http://localhost:3000/logs');
        
        eventSource.onmessage = (e) => {
            setLogs(prev => [...prev, e.data]);
        };
        
        eventSource.onerror = (e) => {
            console.error('EventSource error:', e);
            eventSource.close();
        };
        
        return () => eventSource.close();
    }, []);

    return (
        <Box sx={{position: 'absolute', width: '1000px', height:'1000px', backgroundColor: "white", color: 'black', top:'50%', left:"50%", transform:'translate(-50%, -50%)', zIndex:'10000'}}>
        <div>
            {logs.map((log, i) => <pre key={i}>{log}</pre>)}
        </div>
        </Box>
    );
}

export default LogStream;