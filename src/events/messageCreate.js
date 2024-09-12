const {inspect} = require('node:util');
const readline = require('node:readline');

function print(...args) {
  for (const arg of args) {
    console.log(
      typeof arg === 'object' ? inspect(arg, false, null, true) : arg
    );
  }
}

module.exports = {
  name: 'messageCreate',
  async execute(message, client) {
    console.log(message.content);
    if (message.author.bot) return;

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.question('Reply:', (answer) => {
      message.channel.send(answer).catch((error) => {
        console.error(error);
        message.channel.send('I was unable to send a message.');
      });

      rl.close();
    });
  },
};
