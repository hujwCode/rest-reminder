# APK打包指南 - Windows用户

由于Buildozer只支持Linux/macOS，Windows用户有以下3种方案：

---

## 🌟 方案1：使用GitHub Actions自动打包（推荐，免费）

这是最简单的方法，完全自动化，不需要安装任何工具。

### 步骤：

1. **将代码上传到GitHub**
   ```bash
   # 在GitHub创建新仓库
   git init
   git add main.py buildozer.spec
   git commit -m "Add mobile app"
   git remote add origin https://github.com/你的用户名/rest-reminder.git
   git push -u origin main
   ```

2. **创建GitHub Actions工作流**

   在仓库中创建文件：`.github/workflows/build.yml`

   ```yaml
   name: Build APK

   on:
     push:
       branches: [ main ]
     workflow_dispatch:

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v3

       - name: Build APK with Buildozer
         uses: ArtemSBulgakov/buildozer-android-action@v1.2.1
         id: buildozer

       - name: Upload APK
         uses: actions/upload-artifact@v3
         with:
           name: apk
           path: ${{ steps.buildozer.outputs.filename }}
   ```

3. **自动构建**
   - 推送代码后，GitHub会自动构建APK
   - 在仓库的"Actions"标签查看进度
   - 构建完成后下载APK文件

4. **下载APK**
   - 进入Actions页面
   - 点击最新的构建任务
   - 在"Artifacts"部分下载APK

**预计时间：15-20分钟**

---

## 📦 方案2：使用Docker（需要安装Docker）

在Windows上使用Docker运行Linux环境进行打包。

### 步骤：

1. **安装Docker Desktop**
   - 下载：https://www.docker.com/products/docker-desktop/
   - 安装并启动Docker

2. **准备打包脚本**

   创建文件 `build_apk_docker.bat`：

   ```batch
   @echo off
   echo Starting Docker build...

   docker run -it --rm ^
     -v "%CD%":/home/user/appcode ^
     -v "%CD%/.buildozer_cache":/home/user/.buildozer_cache ^
     yuvarajbaba/buildozer:latest ^
     bash -c "cd appcode && buildozer -v android debug"

   echo APK should be in bin/ directory
   pause
   ```

3. **运行打包**
   ```batch
   build_apk_docker.bat
   ```

4. **获取APK**
   - 打包完成后，APK在 `bin/` 目录

**预计时间：20-30分钟**

---

## 💻 方案3：使用WSL2（Windows子系统）

使用Windows的Linux子系统进行打包。

### 步骤：

1. **启用WSL2**
   ```powershell
   # 以管理员身份运行PowerShell
   wsl --install
   ```

2. **重启电脑并安装Ubuntu**

3. **在WSL中安装依赖**
   ```bash
   # 打开Ubuntu
   sudo apt update
   sudo apt install -y build-essential git python3 python3-pip
   sudo apt install -y openjdk-17-jdk
   sudo apt install -y automake libtool pkg-config libncurses5-dev

   pip3 install buildozer kivy
   ```

4. **复制代码到WSL**
   ```bash
   # 在WSL中访问Windows文件
   cd /mnt/d/project/休息提醒工具
   ```

5. **打包APK**
   ```bash
   buildozer android debug
   ```

**预计时间：20-30分钟**

---

## 🌐 方案4：在线打包服务

使用第三方在线打包平台：

### 1. **Pytonizer (pytonizer.com)**
   - 访问网站
   - 上传 main.py
   - 自动生成APK
   - 免费有限制

### 2. **Replit (replit.com)**
   - 创建Python项目
   - 上传代码
   - 使用Buildozer打包
   - 免费账户可用

### 3. **Codemagic (codemagic.io)**
   - 支持Kivy项目
   - 免费每月100次构建
   - 配置相对简单

---

## ✅ 最简单的推荐方案

**如果你是新手：** 使用 **方案1 (GitHub Actions)**
- 完全免费
- 自动化
- 不需要本地安装工具

**如果你想要最快：** 使用 **Web版本** (rest_reminder_web.html)
- 无需打包
- 直接在浏览器使用
- 可添加到主屏幕

**如果你需要真正的App：**
- 考虑使用方案1或方案2
- 或者我可以帮你配置自动化构建

---

## 📱 获得APK后

1. 将APK传输到Android手机
2. 设置中启用"允许安装未知来源应用"
3. 点击APK文件安装
4. 首次运行授予必要权限

---

## 🔧 常见问题

**Q: GitHub Actions构建失败？**
A: 检查buildozer.spec配置是否正确，查看Actions日志

**Q: Docker打包很慢？**
A: 首次运行需要下载镜像，后续会快很多

**Q: WSL权限问题？**
A: 使用sudo运行命令，或配置正确的文件权限

---

## 📞 需要帮助？

如果你选择某个方案并遇到问题，告诉我具体的错误信息，我可以帮你解决！
