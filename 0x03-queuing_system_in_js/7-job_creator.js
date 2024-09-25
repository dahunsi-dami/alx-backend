import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Array of jobs
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account'
  }
];

// Loop through the jobs array and create jobs
jobs.forEach(jobData => {
  const job = queue.create('push_notification_code_2', jobData);

  job.on('enqueue', () => {
    console.log(`Notification job created: ${job.id}`);
  });

  job.on('complete', () => {
    console.log(`Notification job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Notification job ${job.id} failed: ${errorMessage}`);
  });

  job.on('progress', (progress) => {
    console.log(`Notification job ${job.id} ${progress}% complete`);
  });

  // Save the job to the queue
  job.save(err => {
    if (err) {
      console.error(`Error saving job: ${err}`);
    }
  });
});

// Process jobs from the queue
queue.process('push_notification_code_2', (job, done) => {
  // Simulate job processing
  const { phoneNumber, message } = job.data;
  
  // Here you can implement your job processing logic
  console.log(`Sending message to ${phoneNumber}: ${message}`);

  // Simulating progress
  let progress = 0;
  const interval = setInterval(() => {
    progress += 20; // Increment progress
    job.progress(progress); // Update job progress

    if (progress >= 100) {
      clearInterval(interval);
      return done(); // Mark job as complete
    }
  }, 1000); // Update progress every second
});