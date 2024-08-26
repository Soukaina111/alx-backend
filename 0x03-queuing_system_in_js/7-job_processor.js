#!/usr/bin/yarn dev

// Import the 'kue' module to create a queue and Job type
import { createQueue, Job } from 'kue';

// Define a list of blacklisted phone numbers
const Black_Nums = ['4153518780', '4153518781'];

// Create a new queue
const queue = createQueue();

/**
 * Sends a push notification to a user.
 * @param {String} phoneNumber - The phone number to send the notification to
 * @param {String} message - The message to include in the notification
 * @param {Job} job - The job object associated with the notification
 * @param {*} done - The callback function to call when the notification is sent
 */
const sendNotification = (phoneNumber, message, job, done) => {
  let total = 2, pending = 2;
  let sendInterval = setInterval(() => {
    // Update the job progress every time half the total number of attempts have been made
    if (total - pending <= total / 2) {
      job.progress(total - pending, total);
    }

    // Check if the phone number is blacklisted
    if (Black_Nums.includes(phoneNumber)) {
      // If the number is blacklisted, call the `done` function with an error
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      clearInterval(sendInterval);
      return;
    }

    // If all attempts have been made, log the notification message
    if (total === pending) {
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`,
      );
    }

    // Decrement the pending attempts and call the `done` function when all attempts are complete
    --pending || done();
    pending || clearInterval(sendInterval);
  }, 1000);
};

// Process jobs of type 'push_notification_code_2' with a concurrency of 2
queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});