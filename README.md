# ServerAutoTestTool

這是一個用來自動化伺服器測試的範例專案。
目前僅包含說明文件，尚未提供具體實作，但以下列出預期的使用流程。

## 安裝

1. 安裝 Python 3.10 以上版本。
2. 下載此專案：
   ```bash
   git clone <repository-url>
   cd ServerAutoTestTool
   ```
3. 如果有 `requirements.txt`，可執行：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方式

1. 在 `tests/` 目錄撰寫 pytest 測試腳本。
2. 於專案根目錄執行：
   ```bash
   pytest
   ```
   即可執行所有測試。
3. 若將來提供主程式，可使用：
   ```bash
   python main.py
   ```
   來啟動自動化測試流程。

## 目錄結構（預期）

```
ServerAutoTestTool/
├── tests/          # 測試腳本放置處
├── src/            # 工具程式碼
├── README.md
```

## 版本

目前仍在初期開發階段，歡迎貢獻或提出建議。
