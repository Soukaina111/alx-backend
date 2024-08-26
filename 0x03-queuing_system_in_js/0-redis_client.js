// Import the Redis client library
import redis from 'redis';

// Create a new Redis client instance
const user = redis.createClient();

// Attach a listener for the 'connect' event
// This event is emitted when the client is connected to the Redis server
user.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Attach a listener for the 'error' event
// This event is emitted when the client encounters an error while connecting to the server
user.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});