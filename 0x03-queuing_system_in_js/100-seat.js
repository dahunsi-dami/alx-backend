import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const reserveSeat = (number) => {
  client.set('available_seats', number);
};

const getCurrentAvailableSeats = promisify(client.get).bind(client);

reserveSeat(50);
let reservationEnabled = true;
