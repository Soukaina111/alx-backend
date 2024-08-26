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
  console.error(`Redis client not connected to the server: ${err}`);
});

// Function to set a new school value
function setNewSchool(schoolName, value) {
    user.set(schoolName, value, redis.print);
}

// Asynchronous function to retrieve school value
async function displaySchoolValue(schoolName) {
  // Promisify the 'get' method
  const getAsync = promisify(client.get).bind(user);
  // Await the promisified 'get' method
  const value = await getAsync(schoolName);
  console.log(value);
}

// Call displaySchoolValue for 'Holberton'
displaySchoolValue('Holberton');
// Call setNewSchool to set a new school value
setNewSchool('HolbertonSanFrancisco', '100');
// Call displaySchoolValue for 'HolbertonSanFrancisco'
displaySchoolValue('HolbertonSanFrancisco');