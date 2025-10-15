import streamlit as st
import json
import time
import random
import os
from datetime import datetime, timezone, timedelta

# 配置常量
CALL_LOG_FILE = "call_log.json"
THREE_DAYS_IN_SECONDS = 3 * 24 * 3600

# 硬编码的学生名单
HARDCODED_ROSTER = [
    "刘海燕",
    "赵晟羽",
    "刘佳欣",
    "周佳旺",
    "郭炳清",
    "任明辉",
    "冯炳栋",
    "管中正",
    "吴冬凡",
    "朱国栋",
    "曾凡政",
    "李哲",
    "韩宜恒",
    "王文洋",
    "覃东",
    "王留根",
    "干雨琪",
    "王剑涛",
    "史景麟",
    "王生远",
    "刘建成",
    "王梅文",
    "李星蒴",
    "舒艾凌",
    "周谊华",
    "张文开",
    "李建行",
    "惠晨宇",
    "朱磊",
    "戴佳乐",
    "粟嘉栋",
    "于成龙",
    "江文杰",
    "谢岩",
    "杜文辉",
    "赵明宽",
    "侯文浩",
    "楼飘豪",
    "陈维昊",
    "徐俊豪",
    "黄程",
    "刘梦飞",
    "周朝乐",
    "莫林丛",
    "王轩",
    "韩雨辰",
    "郭思琦",
    "黄仲秋",
    "聂心雨",
    "张年",
    "姚佳良",
    "雷锦浩",
    "宣智超",
    "曾宇宝",
    "汪建杰",
    "段天博",
    "王子赫",
    "王博",
    "周祎烁",
    "陈鑫",
    "孙塬东",
    "宋越扬",
    "袁执戈",
    "席传鑫",
    "王志博",
    "马学超",
    "王一普",
    "吕济发",
    "方启超",
    "曹杰",
    "侯国华",
    "林贻胜",
    "闫瑞祥",
    "程浩",
    "熊健",
]


# 初始化应用
st.set_page_config(page_title="黑马课堂点名器", page_icon="🎯", layout="wide")


# 页面标题
st.title("🎯 杭州黑马AI大模型开发(python)就业3期课堂点名器")
st.markdown("---")


# 创建数据文件（如果不存在）
def initialize_files():
    """初始化数据文件"""
    # 不再创建roster.json文件
    if not os.path.exists(CALL_LOG_FILE):
        with open(CALL_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


# 加载学生名单
def load_roster():
    """加载学生名单（直接返回硬编码的名单）"""
    return HARDCODED_ROSTER


# 保存学生名单
def save_roster(roster):
    """保存学生名单（不再实际保存到文件）"""
    # 由于使用硬编码名单，此函数可以留空或添加日志
    st.warning("学生名单已硬编码在程序中，无法修改")


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


# 格式化时间戳为可读格式（使用东八区时间）
def format_timestamp(timestamp):
    """格式化时间戳为可读格式（东八区时间）"""
    # 创建东八区时区对象
    tz_beijing = timezone(timedelta(hours=8))
    # 将时间戳转换为UTC时间，然后转换为东八区时间
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(tz_beijing)
    return dt.strftime("%Y-%m-%d %H:%M")


# 主函数
def main():
    # 初始化文件
    initialize_files()

    # 初始化session state
    if "last_called_student" not in st.session_state:
        st.session_state.last_called_student = None
    if "show_balloons" not in st.session_state:
        st.session_state.show_balloons = False

    # 加载数据
    roster = load_roster()
    call_log = load_call_log()

    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎲 点名功能")

        # 显示统计信息
        available_students = get_available_students(roster, call_log)

        st.info(
            f"📊 全部学生：{len(roster)}人 | 可点名学生：{len(available_students)}人"
        )

        # 随机点名按钮
        if st.button("🎯 随机点名（3日内不会重复点名）", key="random_call"):
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

                # 保存点名结果到session state
                st.session_state.last_called_student = selected_student
                st.session_state.show_balloons = True

                # 使用st.rerun()刷新页面以显示更新后的统计数据
                st.rerun()
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

                # 保存点名结果到session state
                st.session_state.last_called_student = selected_student
                st.session_state.show_balloons = True

                # 使用st.rerun()刷新页面以显示更新后的统计数据
                st.rerun()

        # 显示点名结果（放在按钮下方）
        if st.session_state.last_called_student:
            st.markdown(
                f"<h1 style='text-align: center; color: red;'>🎉 {st.session_state.last_called_student} 🎉</h1>",
                unsafe_allow_html=True,
            )

            # 只在需要显示balloons时触发
            if st.session_state.show_balloons:
                st.balloons()
                st.session_state.show_balloons = False  # 重置状态

            # 添加清除点名结果按钮
            if st.button("清除点名结果", key="clear_result"):
                st.session_state.last_called_student = None
                st.rerun()

            # 不要在这里重置状态，让点名结果保持显示
            # st.session_state.last_called_student = None

        st.markdown("---")

        st.subheader("📋 学生名单")

        # 显示当前名单（只读，不换行）
        if roster:
            # 添加CSS样式
            st.markdown(
                """
            <style>
            .student-container {
                background-color: #e6f3ff;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                border: 1px solid #b3d9ff;
            }
            .student-grid {
                display: grid;
                grid-template-columns: repeat(10, 1fr);
                gap: 8px;
            }
            .student-card {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 8px;
                text-align: center;
                font-size: 11px;
                height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
                color: #333333;
            }
            .student-card:hover {
                background-color: #f8f9fa;
                transform: scale(1.05);
                color: #000000;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            # 使用HTML/CSS创建多列网格布局，每行10个学生
            roster_html = '<div class="student-container"><div class="student-grid">'

            for student in roster:
                roster_html += f'<div class="student-card">{student}</div>'

            roster_html += "</div></div>"

            # 显示学生总数
            st.markdown(
                f"<small>👥 共{len(roster)}名学生</small>", unsafe_allow_html=True
            )
            st.markdown(roster_html, unsafe_allow_html=True)
        else:
            st.info("暂无学生名单")

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

        # 清空点名记录按钮
        if st.button("🧹 清空点名记录"):
            st.session_state.confirm_clear = True
            # 移除这里的st.rerun()，避免立即刷新页面

        # 如果需要确认清空，则显示确认和取消按钮
        if st.session_state.confirm_clear:
            st.warning("⚠️ 确认清空所有点名记录？")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ 确认", key="confirm_clear_btn"):
                    call_log.clear()
                    save_call_log(call_log)
                    st.success("点名记录已清空！")
                    st.session_state.confirm_clear = False
                    # 只有在确认清空后才刷新页面
                    st.rerun()
            with col2:
                if st.button("❌ 取消", key="cancel_clear_btn"):
                    st.session_state.confirm_clear = False
                    # 取消时不需要刷新页面
                    st.rerun()


if __name__ == "__main__":
    main()
