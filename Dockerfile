# Python3のイメージを基にする
FROM python:3
ENV PYTHONUNBUFFERED=1

# ビルド時に/codeというディレクトリを作成する
RUN mkdir /code

# ワークディレクトリの設定
WORKDIR /code

# requirements.txtを/code/にコピーする
COPY requirements.txt /code/

# requirements.txtを基に pip installする
RUN pip install -r requirements.txt