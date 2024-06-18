- myST -> Login to your account (allows you to download and install embedded software packages)
  - Help -> Manage Embedded Software Packages (Should auto install STM 32Cube MCU Package for STM32F4 Series v1.28 when you build)
- Help -> ST-Link Upgrade (After connecting STM32F401RE via USB)
  - Open in update mode
  - Upgrade
- If you didn't install ST-Link Server during STM32CubeIDE Setup: https://www.st.com/en/development-tools/st-link-server.html

Import Project:
- File -> Import -> General -> Existing Projects into Workspace
- Open capstone-design-project/board (this folder)
- Should be able to build (hammer icon) and upload to STM32F401RE (Green run/play button)
