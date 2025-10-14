import streamlit as st
import json
import time
import random
import os
from datetime import datetime

# 配置常量
ROSTER_FILE = "roster.json"
CALL_LOG_FILE = "call_log.json"
THREE_DAYS_IN_SECONDS = 3 * 24 * 3600

# 初始化应用
st.set_page_config(page_title="课堂点名器", page_icon="🎯", layout="wide")

# 页面标题
st.title("🎯 杭州黑马AI大模型开发(python)就业3期课堂点名器")
st.markdown("---")


# 创建数据文件（如果不存在）
def initialize_files():
    """初始化数据文件"""
    if not os.path.exists(ROSTER_FILE):
        with open(ROSTER_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    if not os.path.exists(CALL_LOG_FILE):
        with open(CALL_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


# 加载学生名单
def load_roster():
    """加载学生名单"""
    try:
        with open(ROSTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# 保存学生名单
def save_roster(roster):
    """保存学生名单"""
    with open(ROSTER_FILE, "w", encoding="utf-8") as f:
        json.dump(roster, f, ensure_ascii=False, indent=2)


# 加载点名记录
def load_call_log():
    """加载点名记录"""
    try:
        with open(CALL_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# 保存点名记录
def save_call_log(call_log):
    """保存点名记录"""
    with open(CALL_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(call_log, f, ensure_ascii=False, indent=2)


# 获取最近3天内被点过名的学生
def get_recently_called_students(call_log):
    """获取最近3天内被点过名的学生"""
    current_time = time.time()
    recently_called = []

    for student, timestamp in call_log.items():
        if current_time - timestamp < THREE_DAYS_IN_SECONDS:
            recently_called.append(student)

    return recently_called


# 获取可点名的学生列表
def get_available_students(roster, call_log):
    """获取可点名的学生列表（排除最近3天内被点过的）"""
    recently_called = get_recently_called_students(call_log)
    return [student for student in roster if student not in recently_called]


# 格式化时间戳为可读格式
def format_timestamp(timestamp):
    """格式化时间戳为可读格式"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M")


# 主函数
def main():
    # 初始化文件
    initialize_files()

    # 加载数据
    roster = load_roster()
    call_log = load_call_log()

    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 学生名单管理")

        # 显示当前名单
        roster_text = "\n".join(roster) if roster else ""
        edited_roster = st.text_area(
            "编辑学生名单（每行一个名字）", value=roster_text, height=200
        )

        # 保存名单按钮
        if st.button("💾 保存名单"):
            # 处理输入的名单
            new_roster = [
                name.strip() for name in edited_roster.split("\n") if name.strip()
            ]
            save_roster(new_roster)
            st.success(f"✅ 名单已保存，共 {len(new_roster)} 名学生")
            # 重新加载名单
            roster = new_roster

        st.markdown("---")

        st.subheader("🎲 点名功能")

        # 显示统计信息
        available_students = get_available_students(roster, call_log)
        st.info(
            f"📊 全部学生：{len(roster)}人 | 可点名学生：{len(available_students)}人"
        )

        # 随机点名按钮
        if st.button("🎯 随机点名", key="random_call"):
            if not roster:
                st.warning("⚠️ 学生名单为空，请先添加学生")
            elif not available_students:
                st.success("✅ 所有同学近 3 天都已点过名！")
                st.info("💡 可使用下方的强制点名功能")
            else:
                # 随机选择一名学生
                selected_student = random.choice(available_students)

                # 更新点名记录
                call_log[selected_student] = time.time()
                save_call_log(call_log)

                # 显示结果（大号字体+醒目颜色）
                st.markdown(
                    f"<h1 style='text-align: center; color: red;'>🎉 {selected_student} 🎉</h1>",
                    unsafe_allow_html=True,
                )
                st.balloons()

        # 强制点名按钮
        if st.button("💪 强制点名（忽略时间限制）", key="force_call"):
            if not roster:
                st.warning("⚠️ 学生名单为空，请先添加学生")
            else:
                # 随机选择一名学生（不考虑时间限制）
                selected_student = random.choice(roster)

                # 更新点名记录
                call_log[selected_student] = time.time()
                save_call_log(call_log)

                # 显示结果（大号字体+醒目颜色）
                st.markdown(
                    f"<h1 style='text-align: center; color: red;'>🎉 {selected_student} 🎉</h1>",
                    unsafe_allow_html=True,
                )
                st.balloons()

    with col2:
        st.subheader("📝 最近点名记录")

        # 显示最近点名记录（最多10条）
        if call_log:
            # 按时间倒序排列
            sorted_logs = sorted(call_log.items(), key=lambda x: x[1], reverse=True)[
                :10
            ]

            # 构建显示数据
            log_data = []
            for student, timestamp in sorted_logs:
                log_data.append(
                    {"学生姓名": student, "点名时间": format_timestamp(timestamp)}
                )

            # 显示表格
            st.table(log_data)
        else:
            st.info("暂无点名记录")

        st.markdown("---")

        # 清空点名记录
        st.subheader("🗑️ 记录管理")

        # 使用确认机制防止误操作
        if "confirm_clear" not in st.session_state:
            st.session_state.confirm_clear = False

        if not st.session_state.confirm_clear:
            if st.button("🧹 清空点名记录"):
                st.session_state.confirm_clear = True
                st.warning("⚠️ 再次点击确认清空所有点名记录")
                st.experimental_rerun()
        else:
            col_confirm1, col_confirm2 = st.columns(2)
            with col_confirm1:
                if st.button("✅ 确认清空"):
                    call_log.clear()
                    save_call_log(call_log)
                    st.session_state.confirm_clear = False
                    st.success("✅ 点名记录已清空")
                    st.experimental_rerun()
            with col_confirm2:
                if st.button("❌ 取消"):
                    st.session_state.confirm_clear = False
                    st.experimental_rerun()


if __name__ == "__main__":
    main()
