// Import the Redis client library
import redis from 'redis';

// Create a new Redis client instance
const user = redis.createClient();

// Attach a listener for the 'connect' event
// This event is emitted when the user is connected to the Redis server
user.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Attach a listener for the 'error' event
// This event is emitted when the user encounters an error while connecting to the server
user.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Define a function to set a new school value in Redis
function setNewSchool(schoolName, value) {
  // Use the client's `set` method to store the school name and value in Redis
  // The `redis.print` function is a callback that logs the result of the operation
  user.set(schoolName, value, redis.print);
}

// Define a function to retrieve the value of a school from Redis
function displaySchoolValue(schoolName) {
  // Use the user's `get` method to retrieve the value for the given school name
  // The callback function will be called with any error and the retrieved value
  user.get(schoolName, (err, reply) => {
    // Log the retrieved value to the console
    console.log(reply);
  });
}

// Call the `displaySchoolValue` function to get the value for 'Holberton'
displaySchoolValue('Holberton');

// Call the `setNewSchool` function to store a new school value
setNewSchool('HolbertonSanFrancisco', '100');

// Call the `displaySchoolValue` function to get the value for 'HolbertonSanFrancisco'
displaySchoolValue('HolbertonSanFrancisco');