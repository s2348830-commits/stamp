const { spawn } = require('child_process');
const http = require('http');

/**
 * 1. Webサーバー設定
 * cron-job.org からの /api へのアクセスに応答します
 */
const server = http.createServer((req, res) => {
    // ルート(/) または /api へのアクセスを許可
    if (req.url === '/' || req.url === '/api') {
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('OK: Bot is active\n');
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

// Renderのポート、またはデフォルト8080を使用
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Monitoring server is running on port ${PORT}`);
});

/**
 * 2. Bot起動ロジック
 */
const startBot = () => {
    console.log('Starting bot.py...');
    
    // Render環境では python3 を指定するのが一般的です
    const botProcess = spawn('python3', ['bot.py']);

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