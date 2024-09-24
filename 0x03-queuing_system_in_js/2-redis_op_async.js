import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', function () {
  console.log('Redis client connected to the server');
});

client.on('error', function (error) {
  console.error('Redis client not connected to the server:', error.message);
});

const getAsync = promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
};

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (error) {
    console.error(`${error.message}`);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
