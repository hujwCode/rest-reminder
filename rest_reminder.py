#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
休息提醒工具
功能：定时弹窗提醒休息，可自定义时间间隔
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime


class RestReminderApp:
    """休息提醒主应用"""

    def __init__(self, root):
        """
        初始化应用对象
        参数:
            root: Tkinter根窗口对象
        功能:
            1. 保存根窗口引用
            2. 设置窗口标题和尺寸
            3. 初始化默认设置（默认提醒间隔60分钟）
            4. 初始化运行状态标志（False表示未运行）
            5. 初始化计时器线程对象（None表示未创建）
            6. 调用create_widgets方法构建界面
        """
        self.root = root
        self.root.title("休息提醒工具")
        self.root.geometry("400x300")

        # 默认设置
        self.default_minutes = 60  # 默认60分钟
        self.is_running = False
        self.timer_thread = None

        self.create_widgets()

    def create_widgets(self):
        """
        创建界面组件
        构建GUI界面的所有元素，包括标题、时间输入框、预设按钮、控制按钮等
        """
        # 标题 - 显示应用名称和图标
        title_label = tk.Label(
            self.root,
            text="💤 休息提醒工具",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=20)

        # 时间设置框架 - 包含标签和输入框，用于设置提醒间隔
        time_frame = tk.Frame(self.root)
        time_frame.pack(pady=10)

        tk.Label(
            time_frame,
            text="提醒间隔（分钟）：",
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT, padx=5)

        self.time_entry = tk.Entry(time_frame, width=10, font=("微软雅黑", 10))
        self.time_entry.insert(0, str(self.default_minutes))
        self.time_entry.pack(side=tk.LEFT, padx=5)

        # 预设时间按钮 - 提供常用的时间间隔快速选择
        preset_frame = tk.Frame(self.root)
        preset_frame.pack(pady=10)

        presets = [("30分钟", 30), ("1小时", 60), ("1.5小时", 90), ("2小时", 120)]

        for text, minutes in presets:
            btn = tk.Button(
                preset_frame,
                text=text,
                command=lambda m=minutes: self.set_time(m),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=5)

        # 控制按钮 - 开始和停止按钮，控制提醒的启动和停止
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.start_button = tk.Button(
            button_frame,
            text="开始提醒",
            command=self.start_reminder,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 12, "bold"),
            width=12
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(
            button_frame,
            text="停止",
            command=self.stop_reminder,
            bg="#f44336",
            fg="white",
            font=("微软雅黑", 12, "bold"),
            width=12,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # 状态显示 - 显示当前提醒是否正在运行
        self.status_label = tk.Label(
            self.root,
            text="状态：未启动",
            font=("微软雅黑", 10),
            fg="#666"
        )
        self.status_label.pack(pady=10)

        # 测试按钮 - 用于测试提醒弹窗效果
        test_button = tk.Button(
            self.root,
            text="测试弹窗",
            command=self.show_reminder_popup,
            font=("微软雅黑", 9)
        )
        test_button.pack(pady=5)

    def set_time(self, minutes):
        """
        设置时间
        参数:
            minutes (int): 要设置的分钟数
        功能:
            清空输入框并填入指定的时间值
        """
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, str(minutes))

    def start_reminder(self):
        """
        开始提醒
        功能:
            1. 从输入框获取用户设置的分钟数
            2. 验证输入的有效性（必须为正整数）
            3. 更新界面状态（禁用开始按钮，启用停止按钮）
            4. 创建并启动计时器线程
            5. 将主窗口最小化到任务栏
        异常处理:
            ValueError: 当输入非数字内容时弹出错误提示
        """
        try:
            minutes = int(self.time_entry.get())
            if minutes <= 0:
                messagebox.showerror("错误", "请输入大于0的时间！")
                return

            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(
                text=f"状态：运行中（每{minutes}分钟提醒）",
                fg="#4CAF50"
            )

            # 启动计时器线程
            self.timer_thread = threading.Thread(
                target=self.reminder_loop,
                args=(minutes,),
                daemon=True
            )
            self.timer_thread.start()

            # 最小化主窗口
            self.root.iconify()

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")

    def stop_reminder(self):
        """
        停止提醒
        功能:
            1. 将运行状态标志设为False，停止计时器线程
            2. 恢复界面按钮状态（启用开始按钮，禁用停止按钮）
            3. 更新状态标签显示为"已停止"
        """
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态：已停止", fg="#f44336")

    def reminder_loop(self, minutes):
        """
        提醒循环
        参数:
            minutes (int): 提醒间隔的分钟数
        功能:
            1. 将分钟转换为秒
            2. 进入while循环，每隔指定时间睡眠一次
            3. 每次睡眠结束后检查运行状态
            4. 如果仍在运行，则显示提醒弹窗
            5. 循环往复，直到is_running变为False
        注意:
            此方法在独立线程中运行，不阻塞主界面
        """
        seconds = minutes * 60

        while self.is_running:
            time.sleep(seconds)

            if not self.is_running:
                break

            # 显示提醒弹窗
            self.show_reminder_popup()

    def show_reminder_popup(self):
        """
        显示提醒弹窗（置顶）
        功能:
            1. 创建一个新的Toplevel窗口作为提醒弹窗
            2. 设置窗口为置顶状态，确保用户能看到
            3. 设置窗口大小为500x350，不可调整大小
            4. 将窗口居中显示在屏幕中央
            5. 创建绿色背景的内容框架
            6. 显示休息图标、标题、提示内容列表
            7. 显示当前时间
            8. 提供两个按钮："我知道了"和"5分钟后"
            9. 尝试播放系统提示音
        """
        # 创建新窗口 - Toplevel创建独立的顶级窗口
        popup = tk.Toplevel()
        popup.title("休息提醒 💤")

        # 设置窗口置顶 - 使用-topmost属性确保窗口始终在最前面
        popup.attributes('-topmost', True)
        popup.lift()  # 将窗口提升到最顶层
        popup.focus_force()  # 强制获取键盘焦点

        # 设置窗口大小和位置 - 固定大小500x350，不可调整
        popup.geometry("500x350")
        popup.resizable(False, False)

        # 居中显示 - 计算屏幕中心坐标，将窗口放置在屏幕中央
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')

        # 内容框架 - 绿色背景的容器，用于放置所有界面元素
        content_frame = tk.Frame(popup, bg="#E8F5E9")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 图标和标题 - 显示咖啡杯图标和主要标题文字
        icon_label = tk.Label(
            content_frame,
            text="☕",
            font=("Arial", 48),
            bg="#E8F5E9"
        )
        icon_label.pack(pady=10)

        title_label = tk.Label(
            content_frame,
            text="该休息一下啦！",
            font=("微软雅黑", 20, "bold"),
            bg="#E8F5E9",
            fg="#2E7D32"
        )
        title_label.pack(pady=10)

        # 提示内容 - 显示具体的休息建议列表
        tips = [
            "🔸 站起来走动走动",
            "🔸 远眺放松眼睛",
            "🔸 喝杯水补充水分",
            "🔸 做个简单的伸展运动"
        ]

        for tip in tips:
            tip_label = tk.Label(
                content_frame,
                text=tip,
                font=("微软雅黑", 12),
                bg="#E8F5E9"
            )
            tip_label.pack(pady=5, anchor="w")

        # 时间显示 - 显示当前的具体时间
        time_label = tk.Label(
            content_frame,
            text=f"当前时间：{datetime.now().strftime('%H:%M:%S')}",
            font=("微软雅黑", 10),
            bg="#E8F5E9",
            fg="#666"
        )
        time_label.pack(pady=15)

        # 按钮区域 - 包含"我知道了"和"5分钟后"两个操作按钮
        button_frame = tk.Frame(content_frame, bg="#E8F5E9")
        button_frame.pack(pady=10)

        def close_popup():
            """
            关闭弹窗
            功能: 销毁弹窗窗口对象
            """
            popup.destroy()

        def snooze():
            """
            稍后提醒功能（贪睡模式）
            功能:
                1. 关闭当前弹窗
                2. 创建一个新的线程，睡眠5分钟（300秒）
                3. 5分钟后如果提醒仍在运行，再次显示提醒弹窗
            """
            popup.destroy()
            # 5分钟后再提醒
            threading.Thread(
                target=lambda: (
                    time.sleep(300),
                    self.show_reminder_popup() if self.is_running else None
                ),
                daemon=True
            ).start()

        ok_button = tk.Button(
            button_frame,
            text="我知道了",
            command=close_popup,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 11, "bold"),
            width=12,
            height=1
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        snooze_button = tk.Button(
            button_frame,
            text="5分钟后",
            command=snooze,
            bg="#FF9800",
            fg="white",
            font=("微软雅黑", 11, "bold"),
            width=12,
            height=1
        )
        snooze_button.pack(side=tk.LEFT, padx=5)

        # 播放提示音 - 使用系统默认提示音吸引注意
        try:
            popup.bell()  # bell()方法播放系统提示音
        except:
            pass  # 如果播放失败，静默处理，不影响程序运行

        # 保持窗口在最前面 - 再次确保置顶属性生效
        popup.attributes('-topmost', True)


def main():
    """
    主函数 - 程序入口点
    功能:
        1. 创建Tkinter根窗口对象
        2. 实例化RestReminderApp应用对象
        3. 注册窗口关闭回调函数
        4. 启动主事件循环，保持窗口运行
    """
    root = tk.Tk()
    app = RestReminderApp(root)

    # 关闭窗口时停止计时器
    def on_closing():
        """
        窗口关闭事件处理函数
        功能:
            1. 将提醒运行状态设为False，停止后台计时线程
            2. 销毁主窗口，退出程序
        """
        app.is_running = False
        root.destroy()

    # 注册窗口关闭协议，当用户点击关闭按钮时调用on_closing函数
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()