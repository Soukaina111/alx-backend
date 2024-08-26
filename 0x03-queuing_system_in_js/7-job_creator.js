#!/usr/bin/yarn dev

// Import the 'kue' module to create a queue
import { createQueue } from 'kue';

// Define an array of job information objects
const works = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  // Additional job objects...
];

// Create a new queue with the name 'push_notification_code_2'
const queue = createQueue({ name: 'push_notification_code_2' });

// Loop through the jobs array and create a new job for each
for (const dataW of works) {
  const work = queue.create('push_notification_code_2', dataW);

  // Add event listeners to the job
  work
    .on('enqueue', () => {
      // Log a message when the job is created
      console.log('Notification job created:', work.id);
    })
    .on('complete', () => {
      // Log a message when the job is completed
      console.log('Notification job', work.id, 'completed');
    })
    .on('failed', (err) => {
      // Log a message when the job fails
      console.log('Notification job', work.id, 'failed:', err.message || err.toString());
    })
    .on('progress', (progress, _data) => {
      // Log the progress of the job
      console.log('Notification job', work.id, `${progress}% complete`);
    });

  // Save the job to the queue
  work.save();
}