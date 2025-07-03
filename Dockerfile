########################
# 1️⃣ 基礎映像（Base） #
########################
# 用 slim 版減少體積；記得在 CI/CD 裡的 Python 版本對齊（3.11）
FROM python:3.11-slim AS base

# 設定時區 & 語言
ENV TZ=Asia/Taipei \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential git curl && \
    pip install --upgrade pip && \
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 建一個非 root 使用者，安全也避免 HF Space 部署失敗
RUN useradd -m -u 1000 appuser
WORKDIR /app
USER appuser

#########################
# 2️⃣ 安裝 Python 套件   #
#########################
# 拆成 two-stage layer：先複製 requirements 以利用快取
COPY --chown=appuser:appuser requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

##########################
# 3️⃣ 複製程式 & 模型檔   #
##########################
# 建議把 models/ data/ 放 .gitignore，改為 start-up 時下載或 HF Hub pull
COPY --chown=appuser:appuser . .

##########################
# 4️⃣ 執行指令 (CMD/EXPOSE)#
##########################
# HF Space (Docker 型) 會讀取埠號 7860；如果是 FastAPI/UIvicorn，可改 8000
EXPOSE 7860

# --- Gradio ---
CMD ["python", "app.py"]