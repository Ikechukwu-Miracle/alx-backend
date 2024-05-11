import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err.message}`);
});

const KEY = "HolbertonSchools";

const keyWords = ["Portland", "Seattle", "New York", "Bogota", "Cali", "Paris"];
const keyValues = [50, 80, 20, 20, 40, 2];

keyWords.forEach((keyElement, index) => {
    client.hset(KEY, keyElement, keyValues[index], redis.print);
});

client.hgetall('HolbertonSchools', (err, reply) => {
    if (err) {
      console.error(`Error getting hash: ${err}`);
      return;
    }
    console.log(reply);
  });
