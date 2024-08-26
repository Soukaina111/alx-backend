#!/usr/bin/yarn dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const logi = express();
const user = createClient({ name: 'reserve_seat' });
const queue = createQueue();
const INITIAL_SEATS_COUNT = 50;
let ReserOK = false;
const PORT = 1245;

/**
 * Modifies the number of available seats.
 * @param {number} number - The new number of seats.
 */
const reserveSeat = async (number) => {
  return promisify(client.SET).bind(user)('available_seats', number);
};

/**
 * Retrieves the number of available seats.
 * @returns {Promise<String>}
 */
const DispoSeats = async () => {
  return promisify(user.GET).bind(user)('available_seats');
};

logi.get('/available_seats', (_, res) => {
  DispoSeats()
    // .then(result => Number.parseInt(result || 0))
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats })
    });
});

logi.get('/reserve_seat', (_req, res) => {
  if (!ReserOK) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');

    job.on('failed', (err) => {
      console.log(
        'Seat reservation job',
        job.id,
        'failed:',
        err.message || err.toString(),
      );
    });
    job.on('complete', () => {
      console.log(
        'Seat reservation job',
        job.id,
        'completed'
      );
    });
    job.save();
    res.json({ status: 'Reservation in process' });
  } catch {
    res.json({ status: 'Reservation failed' });
  }
});

logi.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', (_job, done) => {
    DispoSeats()
      .then((result) => Number.parseInt(result || 0))
      .then((availableSeats) => {
        ReserOK = availableSeats <= 1 ? false : ReserOK;
        if (availableSeats >= 1) {
          reserveSeat(availableSeats - 1)
            .then(() => done());
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

const resetAvailableSeats = async (initialSeatsCount) => {
  return promisify(client.SET)
    .bind(user)('available_seats', Number.parseInt(initialSeatsCount));
};

logi.listen(PORT, () => {
  resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT)
    .then(() => {
      ReserOK = true;
      console.log(`API available on localhost port ${PORT}`);
    });
});

export default logi;