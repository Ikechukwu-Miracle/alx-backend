const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const redisClient = redis.createClient();
const reserveSeat = promisify(redisClient.set).bind(redisClient);
const getCurrentAvailableSeats = promisify(redisClient.get).bind(redisClient);

// Kue queue
const queue = kue.createQueue();

// Initialize available seats to 50
reserveSeat('available_seats', 50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Middleware to ensure JSON response
app.use(express.json());

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats('available_seats');
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save(err => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats('available_seats');
  if (parseInt(numberOfAvailableSeats) === 0) {
    reservationEnabled = false;
  }

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats('available_seats');
    if (parseInt(currentSeats) > 0) {
      await reserveSeat('available_seats', parseInt(currentSeats) - 1);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });

  res.json({ status: 'Queue processing' });
});

// Event listener for successful job completion
queue.on('job complete', (id) => {
  console.log(`Seat reservation job ${id} completed`);
});

// Event listener for failed job
queue.on('job failed', (id, err) => {
  console.log(`Seat reservation job ${id} failed: ${err}`);
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

module.exports = app; // Export app for testing purposes
