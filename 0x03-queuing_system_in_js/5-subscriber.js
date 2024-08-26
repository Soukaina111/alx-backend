// Import Redis client library
import redis from 'redis';
// Import promisify utility from 'util' module
import { promisify } from 'util';

// Create new Redis client instance
const user = redis.createClient();

// Handle connection event
user.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle error event
user.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the 'holberton school channel'
user.subscribe('holberton school channel');

// Handle message event
user.on('message', (channel, message) => {
  console.log(message);
  // If the message is 'KILL_SERVER', unsubscribe and disconnect the client
  if (message === 'KILL_SERVER') {
    user.unsubscribe();
    user.quit();
  }
});

// Asynchronous function to publish a message after a specified delay
async function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    user.publish('holberton school channel', message);
  }, time);
}

// Publish messages with different delays
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);