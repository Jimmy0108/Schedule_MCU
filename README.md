 # 排程應用程式 (Schedule MCU)
 
 這是一個基於 Vue.js 和 Vite 開發的排程應用程式。它提供了一個視覺化的介面來管理與排定 MCU (可能是指 Microcontroller Unit 或其他特定領域的縮寫) 的時程。
 
 主要特色是能夠將排程表匯出為 PNG 圖片或 PDF 文件，方便分享與存檔。
 
 ## 功能特色
 
 *   **視覺化排程介面**：透過網頁介面輕鬆安排與檢視時程。
 *   **圖片匯出**：可將目前的排程畫面轉換為 PNG 圖片。
 *   **PDF 匯出**：可將排程表匯出為高品質的 PDF 文件。
 *   **快速開發**：採用 Vite 作為建置工具，提供極速的開發體驗。
 *   **一鍵部署**：整合 `gh-pages`，方便部署到 GitHub Pages。
 
 ## 環境需求
 
 在開始之前，請確保您的開發環境中已安裝以下軟體：
 
 *   Node.js (建議版本 18.x 或以上)
 *   npm 或 yarn / pnpm 套件管理器
 
 ## 安裝與設定
 
 依照以下步驟來設定您的開發環境：
 
 1.  **複製專案儲存庫**
     ```bash
     git clone <您的儲存庫 URL>
     ```
 
 2.  **進入專案目錄**
     ```bash
     cd vue-project
     ```
 
 3.  **安裝相依套件**
     使用 npm:
     ```bash
     npm install
     ```
     或者使用 yarn:
     ```bash
     yarn install
     ```
 
 ## 操作指南
 
 ### 開發模式
 
 執行以下指令以啟動開發伺服器：
 
 ```bash
 npm run dev
 ```
 
 接著在瀏覽器中開啟顯示的 URL (通常是 `http://localhost:5173`) 即可看到應用程式。在開發模式下，任何程式碼的變更都會即時反應在瀏覽器上。
 
 ### 建置專案
 
 當您準備好部署應用程式時，可以執行建置指令：
 
 ```bash
 npm run build
 ```
 
 這個指令會將所有優化過的靜態檔案打包到 `dist` 資料夾中。
 
 ### 部署至 GitHub Pages
 
 專案已設定好 `gh-pages` 套件，您可以透過以下指令將 `dist` 資料夾的內容部署到 GitHub Pages：
 
 ```bash
 npm run deploy
 ```
 
 > **注意**: 在部署前，請確保您已經在 `vite.config.js` 中設定了正確的 `base` 路徑 (通常是您的 GitHub repository 名稱)。
 
 ## 主要使用套件
 
 這個專案的核心功能由以下幾個關鍵套件所構成：
 
 *   **Vue.js**: 核心前端框架。
 *   **Vite**: 新一代前端建置工具，提供快速的開發伺服器與優化的建置流程。
 *   **html-to-image**: 用於將 HTML DOM 節點轉換為圖片。
 *   **html2pdf.js**: 基於 `html2canvas` 和 `jspdf`，用於將 HTML 內容匯出為 PDF。
 *   **gh-pages**: 用於將專案部署到 GitHub Pages 的工具。
