# Emma-HW3

1. 安裝 [Python3](https://www.python.org/downloads/)
2. 在此目錄下

```sh
$ pip install -r requirements.txt
$ python main.py
```

### 結構

```
HW3
├── BOOK                // 參考的講義
├── EXCEL               // 資料存成 CSV，方便自己觀看
├── OUTPUT              // 計算結果的圖檔放置區
├── VIX                 // 從 CBOE 下載的公司 VIX 資料
├── .gitignore          // 不影響
├── main.py             // 主要程式碼
├── README.md           // 說明文件（就是你現在看的）
└── requirements.txt    // 安裝 package 的檔案
```

### 概念釐清

> 題目中提到的 pandas-datareader 是一個 API
>
> 讓你直接從「資料端」獲取股價資訊
>
> 而所謂爬蟲，是指從「網頁端」抓取資料
>
> 兩個為不同的東西
