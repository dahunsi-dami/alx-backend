import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
async function reserveSeat(number) {
  const setAsync = promisify(client.set).bind(client);
  await setAsync('available_seats', number);
};

async function getCurrentAvailableSeats() {
  const getAsync = promisify(client.get).bind(client);
  const seats = await getAsync('available_seats');
  return seats;
};

reserveSeat(50);
let reservationEnabled = true;

import kue from 'kue';
const queue = kue.createQueue();

import express from 'express';
const app = express();
const PORT = 1245;

app.get('/available_seats', async (req, res) => {
  try {
    const seats = await getCurrentAvailableSeats('available_seats');
    res.json({ numberOfAvailableSeats: seats });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error });
  };
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  };

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      return res.json({ status: 'Reservation in process' });
    };
    res.json({ status: 'Reservation failed' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let seats = await getCurrentAvailableSeats();
    seats = parseInt(seats, 10);

    if (seats > 0) {
      reserveSeat(seats - 1);
      if (seats - 1 === 0) {
        reservationEnabled = false;
      };
      done();
    } else {
      done(new Error('Not enough seats available'));
    };
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
