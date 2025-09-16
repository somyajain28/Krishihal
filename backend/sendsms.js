// send-sms.js
require('dotenv').config();
const twilio = require('twilio');

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const client = new twilio(accountSid, authToken);

const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;
const personalPhoneNumber = process.env.YOUR_PERSONAL_PHONE_NUMBER;

client.messages
    .create({
        body: 'Hello from Node.js and Twilio!',
        from: twilioPhoneNumber,
        to: personalPhoneNumber,
    })
    .then(message => console.log(message.sid))
    .catch(err => console.error(err));