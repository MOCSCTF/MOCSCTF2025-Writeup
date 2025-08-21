// (可选) 加载 .env 文件中的环境变量
require('dotenv').config();

const express = require('express');
const fs = require('fs').promises; // 使用 Promise 版本的 fs
const path = require('path');
const cors = require('cors');

const app = express();
// 从环境变量获取端口，或使用默认值 5000
const PORT = process.env.SERVER_PORT || 5000;
// 从环境变量获取密钥，或使用默认值 (!!极不推荐在代码中硬编码密钥!!)
const API_SECRET = process.env.LEADERBOARD_API_SECRET || 'YOUR_DEFAULT_SUPER_SECRET_KEY'; // 强烈建议使用环境变量

const LEADERBOARD_FILE = path.join(__dirname, 'leaderboard.json');

// --- 中间件 ---

// 允许跨域请求 (根据需要调整配置)
// 在开发中，React 应用通常在不同端口 (如 3000)，需要 CORS
app.use(cors());

// 解析请求体中的 JSON 数据
app.use(express.json());

// --- 辅助函数 ---

// 读取排行榜文件
async function readLeaderboard() {
    try {
        // 检查文件是否存在 + 权限 (保留)
        await fs.access(LEADERBOARD_FILE);
        // 读取文件内容 (保留)
        const data = await fs.readFile(LEADERBOARD_FILE, 'utf-8');

        // --- 新增检查：判断文件内容是否为空或只有空白 ---
        if (data.trim() === '') {
            console.log('leaderboard.json is empty or contains only whitespace, returning empty array.');
            return []; // 如果为空，直接返回空数组
        }
        // --- 结束新增检查 ---

        // 只有在文件内容非空时才尝试解析 JSON
        try {
            return JSON.parse(data);
        } catch (parseError) {
            // 如果文件存在但内容不是有效的 JSON (非空但格式错误)
            if (parseError instanceof SyntaxError) {
                console.warn('leaderboard.json contains invalid JSON content, returning empty array. Error:', parseError.message);
                return []; // 对无效 JSON 也返回空数组
            }
            // 抛出其他可能的解析错误 (虽然不太常见)
            throw parseError;
        }

    } catch (error) {
        // 处理文件不存在的情况 (保留)
        if (error.code === 'ENOENT') {
            console.log('leaderboard.json not found, returning empty array.');
            return [];
        }

        // 捕获并记录其他文件读取错误 (如权限问题)
        // 注意：上面的 JSON.parse 错误现在在内部 try/catch 处理了
        console.error('Error accessing or reading leaderboard file:', error);
        // 抛出一个通用错误，让上层 API 路由处理
        throw new Error('Could not read leaderboard data due to file system issue');
    }
}

// 写入排行榜文件
async function writeLeaderboard(data) {
    try {
        await fs.writeFile(LEADERBOARD_FILE, JSON.stringify(data, null, 2), 'utf-8'); // 格式化输出
    } catch (error) {
        console.error('Error writing leaderboard file:', error);
        throw new Error('Could not save leaderboard data');
    }
}

// --- API 密钥验证中间件 ---
// 这个中间件会检查所有 /api/save-score 请求
function authenticate(req, res, next) {
    const providedSecret = req.headers['x-api-secret']; // 从请求头获取密钥

    if (!providedSecret || providedSecret !== API_SECRET) {
        console.warn('Authentication failed: Invalid or missing secret.');
        // 401 Unauthorized: 提供了无效凭证
        // 403 Forbidden: 提供了有效凭证但无权限 (这里用 401 或 403 都可以，401 更贴切些)
        return res.status(401).json({ message: 'Unauthorized: Invalid API Secret' });
    }
    // 密钥正确，继续处理请求
    next();
}


// --- API 路由 ---

// GET /api/leaderboard - 获取排行榜数据 (无需密钥)
app.get('/api/leaderboard', async (req, res) => {
    try {
        const leaderboard = await readLeaderboard();
        res.json(leaderboard);
    } catch (error) {
        res.status(500).json({ message: error.message || 'Failed to retrieve leaderboard' });
    }
});

// POST /api/save-score - 保存新分数 (需要密钥)
// 注意： authenticate 中间件应用在这里
app.post('/api/save-score', authenticate, async (req, res) => {
    const { name, score, duration } = req.body;

    // --- 基本的数据验证 ---
    if (typeof name !== 'string' || name.trim().length === 0 || name.length > 10) {
        return res.status(400).json({ message: 'Invalid name provided.' });
    }
    if (typeof score !== 'number' || !Number.isInteger(score) || score < 0) {
        return res.status(400).json({ message: 'Invalid score provided.' });
    }
    if (typeof duration !== 'number' || duration < 0) {
         // 允许 duration 为 0
        return res.status(400).json({ message: 'Invalid duration provided.' });
    }
    // --- 结束验证 ---

    const newEntry = {
        name: name.trim(),
        score,
        duration,
        date: new Date().toLocaleString('zh-CN', { /* 你的日期格式选项 */ })
    };

    try {
        const leaderboard = await readLeaderboard();

        const updatedLeaderboard = [...leaderboard, newEntry]
            .sort((a, b) => {
                if (b.score !== a.score) return b.score - a.score;
                return a.duration - b.duration;
            })
            .slice(0, 20); // 保留前 20 名

        await writeLeaderboard(updatedLeaderboard);

        // 返回更新后的排行榜和成功消息
        res.status(201).json({ message: 'Score saved successfully!', leaderboard: updatedLeaderboard });

    } catch (error) {
        res.status(500).json({ message: error.message || 'Failed to save score' });
    }
});

// --- （可选）服务 React 应用的静态文件 ---
// 假设你的 React 应用构建后放在 client/build 目录
const buildPath = path.join(__dirname, '..', 'client', 'dist');
console.log(`Serving static files from: ${buildPath}`); // 添加这行方便调试路径问题
app.use(express.static(buildPath));

// --- “兜底”路由，用于客户端路由 ---
// 这个路由应该放在所有 API 路由之后，但在错误处理和服务器启动之前
// 对于所有非 API、非静态文件的 GET 请求，都返回 React 应用的 index.html
app.get('*', (req, res) => {
    const indexPath = path.join(buildPath, 'index.html');
    console.log(`Serving index.html for route: ${req.path}, from: ${indexPath}`); // 添加这行方便调试
    res.sendFile(indexPath, (err) => {
        if (err) {
            console.error('Error sending index.html:', err);
            res.status(500).send(err);
        }
    });
});


// --- 启动服务器 ---
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Leaderboard file path: ${LEADERBOARD_FILE}`);
    if (API_SECRET === 'YOUR_DEFAULT_SUPER_SECRET_KEY') {
         console.warn("WARNING: Using default insecure API secret. Set LEADERBOARD_API_SECRET environment variable!");
    }
});