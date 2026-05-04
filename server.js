const { spawn } = require('child_process');
const http = require('http');

// 1. Render用のシンプルなWebサーバー
// これがないとRenderは「Port 8080 をリッスンしていない」と判断して停止させます
const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Discord Bot is running!\n'); // ここで「生きてるよ」と返します
});

const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});

// 2. bot.py を子プロセスとして起動
const startBot = () => {
    console.log('Starting bot.py...');
    const bot = spawn('python', ['bot.py']);

    bot.stdout.on('data', (data) => {
        console.log(`[Bot]: ${data}`);
    });

    bot.stderr.on('data', (data) => {
        console.error(`[Bot Error]: ${data}`);
    });

    bot.on('close', (code) => {
        console.log(`Bot process exited with code ${code}. Restarting...`);
        startBot(); // 落ちた場合に再起動
    });
};

startBot();