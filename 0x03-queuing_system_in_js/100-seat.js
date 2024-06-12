import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Redis client setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Kue queue setup
const queue = kue.createQueue();

// Express server setup
const app = express();
const port = 1245;

// Initial seat count and reservation state
const initialSeats = 50;
let reservationEnabled = true;

// Utility functions
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats !== null ? parseInt(seats, 10) : null;
}

// Initialize seats
reserveSeat(initialSeats).then(() => console.log('Seats initialized to 50'));

// Routes
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  console.log('Fetching available seats:', seats);
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save(err => {
    if (err) {
      res.json({ status: 'Reservation failed' });
      return;
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    console.log('Processing job:', job.id, 'Current seats:', currentSeats);

    if (currentSeats > 0) {
      await reserveSeat(currentSeats - 1);

      if (currentSeats - 1 === 0) {
        reservationEnabled = false;
        console.log('Reservations disabled: No seats available');
      }

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
