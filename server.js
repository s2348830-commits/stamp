const { spawn } = require('child_process');
const http = require('http');

// Render用のWebサーバー
const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/api') {
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('OK: Bot is active\n');
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});

// Botプロセスを起動
const startBot = () => {
    console.log('Starting bot.py with environment variables...');
    
    // 【重要】env: process.env を追加して、Renderの設定をPythonに渡す
    const botProcess = spawn('python3', ['bot.py'], {
        env: process.env 
    });

    botProcess.stdout.on('data', (data) => {
        console.log(`[Python STDOUT]: ${data}`);
    });

    botProcess.stderr.on('data', (data) => {
        console.error(`[Python STDERR]: ${data}`);
    });

    botProcess.on('close', (code) => {
        console.log(`Bot process exited with code ${code}. Restarting in 5s...`);
        setTimeout(startBot, 5000); 
    });
};

startBot();