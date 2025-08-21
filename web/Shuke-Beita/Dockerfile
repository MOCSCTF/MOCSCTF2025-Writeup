# 使用官方 Node 镜像作为基础 (选择一个明确的 LTS 版本，如 18)
FROM node:18-alpine as builder

# 设置容器内的工作目录
WORKDIR /src

# --- 后端服务器设置 ---
# 复制后端 package.json 和 package-lock.json (或 yarn.lock)
COPY src/server/package*.json ./server/

# 进入后端目录以安装依赖
WORKDIR /src/server

# 只安装生产环境需要的依赖
RUN npm install

# 返回到 /src 根目录
WORKDIR /src

# 复制后端服务器的其余代码 (包括初始的 leaderboard.json, 如果有的话)
COPY src/server/ ./server/

# --- 前端设置 ---
# 复制构建好的前端静态文件
COPY src/client/dist/ ./client/dist/

# --- 最后配置 ---
# 暴露 Node 服务器监听的端口
EXPOSE 5000

# 定义环境变量
ENV NODE_ENV=production
ENV SERVER_PORT=5000
# API_SECRET 仍建议通过 docker-compose 传递

# 定义容器启动时运行的命令
CMD ["node", "server/server.js"]