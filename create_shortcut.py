#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建桌面快捷方式
支持Windows系统
"""

import os
import sys
import platform

def create_shortcut():
    """创建桌面快捷方式"""

    if platform.system() != 'Windows':
        print("此脚本仅支持Windows系统")
        return

    try:
        from win32com.client import Dispatch
        import pythoncom

        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_script = os.path.join(current_dir, "rest_reminder.py")
        batch_file = os.path.join(current_dir, "启动休息提醒.bat")

        # 获取桌面路径
        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')
        desktop_path = shell.SpecialFolders('Desktop')

        # 创建快捷方式
        shortcut_path = os.path.join(desktop_path, "休息提醒.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)

        # 使用批处理文件作为目标（这样会有控制台窗口）
        shortcut.Targetpath = batch_file
        shortcut.WorkingDirectory = current_dir
        shortcut.Description = "定时休息提醒工具 - 保护健康，定时提醒休息"
        shortcut.IconLocation = r"%SystemRoot%\System32\shell32.dll,134"  # 时钟图标

        shortcut.save()

        print("=" * 50)
        print("✅ 快捷方式创建成功！")
        print("=" * 50)
        print(f"快捷方式位置：{shortcut_path}")
        print("\n你现在可以在桌面上看到「休息提醒」图标")
        print("双击即可启动程序！")

    except ImportError:
        print("\n" + "=" * 50)
        print("❌ 缺少必要的库，正在安装...")
        print("=" * 50)

        print("\n请运行以下命令安装所需的库：")
        print("pip install pywin32")

        choice = input("\n是否现在自动安装？(y/n): ").lower()

        if choice == 'y':
            os.system('pip install pywin32')
            print("\n安装完成！请重新运行此脚本")
        else:
            print("\n已取消安装")

    except Exception as e:
        print(f"\n❌ 创建快捷方式失败：{str(e)}")
        print("\n你可以手动创建：")
        print("1. 右键点击桌面 -> 新建 -> 快捷方式")
        print(f"2. 位置输入：{batch_file}")
        print("3. 名称输入：休息提醒")
        print("4. 完成后右键快捷方式 -> 属性 -> 更改图标")


def create_shortcut_simple():
    """简单方法：创建VBScript来生成快捷方式"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    batch_file = os.path.join(current_dir, "启动休息提醒.bat")

    vbs_script = f"""
Set WshShell = CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") & "\\休息提醒.lnk")
Shortcut.TargetPath = "{batch_file}"
Shortcut.WorkingDirectory = "{current_dir}"
Shortcut.Description = "定时休息提醒工具"
Shortcut.IconLocation = "%SystemRoot%\\System32\\shell32.dll,134"
Shortcut.Save

MsgBox "快捷方式创建成功！" & vbCrLf & "请在桌面查看「休息提醒」图标
"""

    vbs_path = os.path.join(current_dir, "create_shortcut.vbs")

    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_script)

    os.system(vbs_path)

    # 删除临时vbs文件
    try:
        os.remove(vbs_path)
    except:
        pass


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("     休息提醒工具 - 创建桌面快捷方式")
    print("=" * 50 + "\n")

    # 先尝试简单方法
    print("正在创建桌面快捷方式...\n")
    create_shortcut_simple()

    input("\n按回车键退出...")