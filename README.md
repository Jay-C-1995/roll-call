# 课堂点名器 🎯

一个基于 Python 和 Streamlit 的课堂点名器应用，具有以下功能：

## 功能特点

- 📋 学生名单管理：可编辑和保存学生名单
- 🎲 智能点名：避免重复点名（3 天内不重复）
- 💪 强制点名：可忽略时间限制进行点名
- 📝 点名记录：显示最近点名历史
- 🗑️ 记录管理：可清空点名记录

## 本地运行

1. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：

   ```bash
   streamlit run roll_call.py
   ```

3. 在浏览器中访问 `http://localhost:8501`

## 部署到 Gitee Pages

1. 将此仓库推送到 Gitee
2. 在 Gitee 仓库中启用 Pages 服务
3. 配置 Pages 使用 Streamlit 构建

## 文件说明

- `roll_call.py`: 主应用程序文件
- `roster.json`: 学生名单数据文件
- `call_log.json`: 点名记录数据文件
- `requirements.txt`: Python 依赖文件

## 使用说明

1. 首次使用时，在左侧文本框中输入学生姓名（每行一个），点击"保存名单"
2. 点击"随机点名"按钮开始点名
3. 可在右侧查看最近的点名记录
