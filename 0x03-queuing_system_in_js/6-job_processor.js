#!/usr/bin/yarn dev

// Import the 'kue' module to create a queue
import { createQueue } from 'kue';

// Create a new queue
const queue = createQueue();

// Define a function to send a notification
const sendNotification = (phoneNumber, message) => {
  console.log(
    `Sending notification to ${phoneNumber},`,
    'with message:',
    message,
  );
};

// Process jobs with the type 'push_notification_code'
queue.process('push_notification_code', (job, done) => {
  // Call the sendNotification function with the job data
  sendNotification(job.data.phoneNumber, job.data.message);
  // Mark the job as completed
  done();
});