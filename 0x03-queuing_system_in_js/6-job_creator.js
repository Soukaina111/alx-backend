#!/usr/bin/yarn dev

// Import the 'kue' module to create a queue
import { createQueue } from 'kue';

// Create a new queue with the name 'push_notification_code'
const queue = createQueue({name: 'push_notification_code'});

// Create a new job in the queue with the type 'push_notification_code'
// and the data 'phoneNumber' and 'message'
const work = queue.create('push_notification_code', {
  phoneNumber: '07045679939',
  message: 'Account registered',
});

// Add event listeners to the job
work
  .on('enqueue', () => {
    // Log a message when the job is created
    console.log('Notification job created:', work.id);
  })
  .on('complete', () => {
    // Log a message when the job is completed
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    // Log a message when the job fails
    console.log('Notification job failed');
  });

// Save the job to the queue
work.save();