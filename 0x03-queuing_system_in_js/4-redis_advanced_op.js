// Import Redis client library
import redis from 'redis';

// Create new Redis client instance
const user = redis.createClient();

// Set multiple key-value pairs in a Redis hash
user.hset("HolbertonSchools", "Portland", 50, redis.print);
user.hset("HolbertonSchools", "Seattle", 80, redis.print);
user.hset("HolbertonSchools", "New York", 20, redis.print);
user.hset("HolbertonSchools", "Bogota", 20, redis.print);
user.hset("HolbertonSchools", "Cali", 40, redis.print);
user.hset("HolbertonSchools", "Paris", 2, redis.print);

// Retrieve all key-value pairs in the "HolbertonSchools" hash
user.hgetall("HolbertonSchools", function(err, reply) {
  console.log(reply);
});