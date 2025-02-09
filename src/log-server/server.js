const Docker = require('dockerode');
const mqtt = require('mqtt');
const docker = new Docker();

const mqttClient = mqtt.connect(process.env.MQTT_BROKER_URL, {
  clientId: 'docker-log-publisher'
});

// Track active log streams
const activeContainers = new Map();

// Connect to MQTT
mqttClient.on('connect', () => {
  console.log('Connected to MQTT broker');
  //startMonitoring();
});

mqttClient.on('error', (err) => {
    console.error('❌ MQTT connection error:', err);
  });
  

// Monitor Docker containers
async function startMonitoring() {
  // Get all running containers
  const containers = await docker.listContainers();
  
  // Start tracking each container
  containers.forEach(containerInfo => {
    trackContainerLogs(containerInfo);
  });

  // Watch for new containers
  const dockerEvents = docker.getEvents();
  dockerEvents.on('data', (chunk) => {
    const event = JSON.parse(chunk.toString());
    if (event.Type === 'container' && event.Action === 'start') {
      docker.getContainer(event.id).inspect()
        .then(containerInfo => trackContainerLogs(containerInfo));
    }
  });
}

// Track logs for a single container
function trackContainerLogs(containerInfo) {
  const container = docker.getContainer(containerInfo.Id);
  const containerName = containerInfo.Names[0].replace(/^\//, ''); // Remove leading slash

  // Skip if already tracking
  if (activeContainers.has(containerName)) return;

  // Start log stream
  const logStream = container.logs({
    follow: true,
    stdout: true,
    stderr: true,
    tail: 0,
    timestamps: true // Include timestamps
  });

  // Process log chunks
  logStream.on('data', (chunk) => {
    parseDockerLog(chunk).forEach(message => {
      const payload = JSON.stringify({
        container: containerName,
        message: message.content,
        timestamp: message.timestamp,
        type: message.type // 'stdout' or 'stderr'
      });

      mqttClient.publish(
        `docker/logs/${containerName}`,
        payload,
        { qos: 1 }
      );
    });
  });

  // Handle stream end
  logStream.on('end', () => {
    activeContainers.delete(containerName);
  });

  // Store reference
  activeContainers.set(containerName, logStream);
}

// Parse Docker's log format (header + message)
function parseDockerLog(chunk) {
  const messages = [];
  for (let i = 0; i < chunk.length; ) {
    const header = chunk.slice(i, i + 8);
    const type = header.readUInt8(0); // 1=stdout, 2=stderr
    const timestamp = new Date(header.readUInt32BE(4) * 1000).toISOString();
    const length = header.readUInt32BE(4);

    messages.push({
      type: type === 1 ? 'stdout' : 'stderr',
      timestamp: timestamp,
      content: chunk.slice(i + 8, i + 8 + length).toString('utf8')
    });

    i += 8 + length;
  }
  return messages;
}

// Cleanup on exit
process.on('SIGINT', () => {
  activeContainers.forEach((stream, name) => {
    stream.destroy();
    console.log(`Stopped tracking ${name}`);
  });
  mqttClient.end();
  process.exit();
});