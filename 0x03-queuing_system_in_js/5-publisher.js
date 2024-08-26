// Import Redis client library
import redis from 'redis';

// Create new Redis client instance
const user = redis.createClient();

// Handle connection event
user.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Handle error event
user.on('error', function(err) {
  console.log('Redis client not connected to the server: ' + err);
});

// Subscribe to the 'holberton school channel'
user.subscribe('holberton school channel');

// Handle message event
user.on('message', function(channel, message) {
  console.log('Message received on channel ' + channel + ': ' + message);
  // If the message is 'KILL_SERVER', unsubscribe and disconnect the client
  if (message === 'KILL_SERVER') {
    user.unsubscribe();
    user.quit();
  }
});