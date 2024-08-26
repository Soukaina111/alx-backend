#!/usr/bin/yarn dev

import { Queue, Job } from 'kue';

const Black_Nums = ['4153518780', '4153518781'];

/**
 * Sends a push notification to a user.
 * @param {String} phoneNumber
 * @param {String} message
 * @param {Job} job
 * @param {*} done
 */
const outputNotif = (phoneNumber, message, job, done) => {
  let total = 2, pending = 2;
  let sendInterval = setInterval(() => {
    if (total - pending <= total / 2) {
      job.progress(total - pending, total);
    }
    if (Black_Nums.includes(phoneNumber)) {
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      clearInterval(sendInterval);
      return;
    }
    if (total === pending) {
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`,
      );
    }
    --pending || done();
    pending || clearInterval(sendInterval);
  }, 1000);
};

/**
 * Creates push notification jobs from the array of jobs info.
 * @param {Job[]} jobs
 * @param {Queue} queue
 */
export const createPushNotificationsJobs = (jobs, queue) => {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }
  for (const jobInfo of jobs) {
    const job = queue.create('push_notification_code_3', jobInfo);

    job
      .on('enqueue', () => {
        console.log('Notification job created:', job.id);
      })
      .on('complete', () => {
        console.log('Notification job', job.id, 'completed');
      })
      .on('failed', (err) => {
        console.log('Notification job', job.id, 'failed:', err.message || err.toString());
      })
      .on('progress', (progress, _data) => {
        console.log('Notification job', job.id, `${progress}% complete`);
      });

    job.save((err) => {
      if (err) {
        console.error('Error saving job:', err);
      } else {
        outputNotif(jobInfo.phoneNumber, jobInfo.message, job, (err) => {
          if (err) {
            console.error('Error sending notification:', err);
          }
        });
      }
    });
  }
};

export default createPushNotificationsJobs;