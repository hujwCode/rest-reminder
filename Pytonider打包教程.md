# Pytonider在线打包APK详细教程

## 步骤1：注册Pytonider

1. 访问：https://pytonizer.com
2. 点击右上角 **"Sign Up"** 或 **"Register"**
3. 使用以下任一方式注册：
   - Google账号
   - GitHub账号
   - 邮箱注册

## 步骤2：创建新项目

1. 登录后点击 **"New Project"** 或 **"+ Create"**
2. 填写项目信息：
   - **Project Name**: `休息提醒` 或 `RestReminder`
   - **Package Name**: `com.restreminder.app` (保持默认格式)
3. 点击 **"Create"** 或 **"Next"**

## 步骤3：上传代码

### 方法A：直接上传文件
1. 点击 **"Upload Files"** 或 **"Add Files"**
2. 选择文件：`main.py`（在 `d:\project\休息提醒工具\` 目录）
3. 点击上传

### 方法B：粘贴代码
1. 点击 **"Create File"**
2. 文件名填：`main.py`
3. 打开 `d:\project\休息提醒工具\main.py`
4. 复制全部内容
5. 粘贴到网页编辑器
6. 点击 **"Save"**

## 步骤4：配置打包选项

1. 选择 **"Python Version"**: `3.9` 或 `3.10`
2. 选择 **"Framework"**: `Kivy`（如果有选项）
3. **App Icon**: 可选上传图标（PNG格式，512x512）
4. 其他选项保持默认

## 步骤5：开始构建

1. 检查所有配置无误
2. 点击 **"Build"** 或 **"Compile"** 或 **"Create APK"**
3. 等待5-10分钟

## 步骤6：下载APK

1. 构建完成后会显示通知
2. 点击 **"Download"** 或 **"Get APK"**
3. APK文件会下载到电脑

## 步骤7：安装到手机

1. 将APK传输到Android手机：
   - 微信/QQ发送给自己
   - 数据线复制
   - 云盘同步

2. 在手机上安装：
   - 找到APK文件
   - 点击安装
   - 允许安装未知来源应用（如提示）
   - 等待安装完成

3. 首次运行：
   - 打开"休息提醒"应用
   - 授予必要权限（震动）
   - 设置提醒时间
   - 点击"开始提醒"

## 常见问题：

### Q: 找不到main.py？
A: 文件在 `d:\project\休息提醒工具\main.py`

### Q: 构建失败？
A:
- 检查Python版本是否选择正确
- 确认上传的是main.py而不是其他文件
- 查看构建日志中的错误信息

### Q: APK签名问题？
A: Pytonider会自动处理签名，无需担心

### Q: 免费版限制？
A:
- 免费版有每日构建次数限制
- 对个人使用完全足够
- 如需更多功能可升级套餐

## 替代方案：

如果Pytonider不行，还可以尝试：

1. **Replit**: https://replit.com
   - 创建Python项目
   - 上传main.py
   - 在Shell中运行 `pip install buildozer && buildozer android debug`

2. **GitHub Codespaces**:
   - 在GitHub仓库页面
   - 点击 "Code" → "Codespaces"
   - 创建Codespace
   - 运行Buildozer命令

3. **本地Docker**:
   - 安装Docker Desktop
   - 使用提供的build_apk.bat脚本

---

**推荐首选Pytonider，最简单快捷！**
