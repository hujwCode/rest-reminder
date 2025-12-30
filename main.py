#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
休息提醒工具 - 移动端版本
支持Android和iOS平台
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.platform import platform
from kivy.core.window import Window
from kivy.utils import platform
from threading import Thread
import time


class MobileReminderApp(App):
    """移动端休息提醒应用"""

    def build(self):
        """构建应用界面"""
        self.title = "休息提醒"
        self.is_running = False
        self.reminder_thread = None
        self.minutes = 60

        # 设置窗口大小（仅在桌面测试时有效）
        if platform != 'android' and platform != 'ios':
            Window.size = (360, 640)

        # 主布局
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 标题
        title = Label(
            text='💤 休息提醒',
            font_size=32,
            size_hint_y=None,
            height=60,
            bold=True
        )
        root.add_widget(title)

        # 说明文字
        desc = Label(
            text='设置提醒间隔，定时休息保护健康',
            font_size=14,
            size_hint_y=None,
            height=40,
            color=(0.5, 0.5, 0.5, 1)
        )
        root.add_widget(desc)

        # 时间输入区域
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        input_layout.add_widget(Label(text='间隔(分钟):', font_size=16, size_hint_x=0.4))

        self.time_input = TextInput(
            text='60',
            font_size=20,
            multiline=False,
            size_hint_x=0.3,
            input_type='number',
            halign='center'
        )
        input_layout.add_widget(self.time_input)
        root.add_widget(input_layout)

        # 预设时间按钮
        preset_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)

        presets = [
            ('30分钟', 30),
            ('1小时', 60),
            ('1.5小时', 90),
            ('2小时', 120)
        ]

        for text, mins in presets:
            btn = Button(
                text=text,
                font_size=14,
                on_release=lambda btn, m=mins: self.set_time(m)
            )
            preset_layout.add_widget(btn)

        root.add_widget(preset_layout)

        # 状态显示
        self.status_label = Label(
            text='状态：未启动',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1)
        )
        root.add_widget(self.status_label)

        # 控制按钮
        button_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=60)

        self.start_btn = Button(
            text='开始提醒',
            font_size=18,
            background_color=(0.2, 0.7, 0.3, 1),
            on_release=self.start_reminder
        )
        button_layout.add_widget(self.start_btn)

        self.stop_btn = Button(
            text='停止',
            font_size=18,
            background_color=(0.9, 0.3, 0.3, 1),
            disabled=True,
            on_release=self.stop_reminder
        )
        button_layout.add_widget(self.stop_btn)

        root.add_widget(button_layout)

        # 测试按钮
        test_btn = Button(
            text='🔔 测试提醒',
            font_size=14,
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.6, 0.9, 1),
            on_release=self.show_reminder_popup
        )
        root.add_widget(test_btn)

        # 版本信息
        version = Label(
            text='移动端 v1.0',
            font_size=12,
            size_hint_y=None,
            height=30,
            color=(0.6, 0.6, 0.6, 1)
        )
        root.add_widget(version)

        return root

    def set_time(self, minutes):
        """设置时间"""
        self.time_input.text = str(minutes)

    def start_reminder(self, instance):
        """开始提醒"""
        try:
            mins = int(self.time_input.text)
            if mins <= 0:
                self.show_error('请输入大于0的时间')
                return

            self.minutes = mins
            self.is_running = True
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.status_label.text = f'状态：运行中（每{mins}分钟）'
            self.status_label.color = (0.2, 0.7, 0.3, 1)

            # 启动提醒线程
            self.reminder_thread = Thread(target=self.reminder_loop, daemon=True)
            self.reminder_thread.start()

        except ValueError:
            self.show_error('请输入有效的数字')

    def stop_reminder(self, instance):
        """停止提醒"""
        self.is_running = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = '状态：已停止'
        self.status_label.color = (0.9, 0.3, 0.3, 1)

    def reminder_loop(self):
        """提醒循环"""
        seconds = self.minutes * 60

        while self.is_running:
            time.sleep(seconds)

            if not self.is_running:
                break

            # 显示提醒
            Clock.schedule_once(lambda dt: self.show_reminder_popup(None), 0)

    def show_reminder_popup(self, instance):
        """显示提醒弹窗"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 图标
        icon = Label(text='☕', font_size=60, size_hint_y=None, height=80)
        content.add_widget(icon)

        # 标题
        title = Label(
            text='该休息一下啦！',
            font_size=24,
            size_hint_y=None,
            height=50,
            bold=True
        )
        content.add_widget(title)

        # 提示内容
        tips = '🔸 站起来走动走动\n🔸 远眺放松眼睛\n🔸 喝杯水补充水分\n🔸 做个简单的伸展运动'
        tips_label = Label(text=tips, font_size=14, halign='left', valign='top')
        content.add_widget(tips_label)

        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        close_btn = Button(
            text='我知道了',
            font_size=16,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        btn_layout.add_widget(close_btn)

        snooze_btn = Button(
            text='5分钟后',
            font_size=16,
            background_color=(1, 0.6, 0, 1)
        )
        btn_layout.add_widget(snooze_btn)

        content.add_widget(btn_layout)

        # 创建弹窗
        popup = Popup(
            title='休息提醒',
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False
        )

        close_btn.bind(on_release=popup.dismiss)
        snooze_btn.bind(on_release=lambda btn: self.snooze_and_close(popup))

        popup.open()

        # 震动提醒（仅Android）
        if platform == 'android':
            try:
                from plyer import vibrator
                vibrator.vibrate(0.5)  # 震动0.5秒
            except:
                pass

    def snooze_and_close(self, popup):
        """稍后提醒"""
        popup.dismiss()
        # 5分钟后再次提醒
        Thread(
            target=lambda: (
                time.sleep(300),
                Clock.schedule_once(lambda dt: self.show_reminder_popup(None), 0)
                if self.is_running else None
            ),
            daemon=True
        ).start()

    def show_error(self, message):
        """显示错误提示"""
        popup = Popup(
            title='错误',
            content=Label(text=message, font_size=16),
            size_hint=(0.7, 0.3)
        )
        popup.open()


if __name__ == '__main__':
    MobileReminderApp().run()
