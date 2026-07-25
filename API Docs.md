آمار OHLC بازار نوبیتکس
curl 'https://apiv2.nobitex.ir/market/udf/history?symbol=BTCIRT&resolution=D&from=1562058167&to=1562230967'
در صورت فراخوانی درست، پاسخ به این صورت خواهد بود:

{
  "s": "ok",
  "t": [1562095800, 1562182200],
  "o": [146272500, 150551000],
  "h": [155869600, 161869500],
  "l": [140062400, 150551000],
  "c": [151440200, 157000000],
  "v": [18.221362316, 9.8592626506]
}
برای توضیحات بیشتر در مورد OHLC به این لینک مراجعه کنید.

برای دریافت آمار OHLC نوبیتکس از این نوع درخواست استفاده نمایید:

درخواست: GET /market/udf/history
پارامترهای ورودی
پارامتر	نوع	پیش‌فرض	توضیحات	نمونه
symbol	string	الزامی	نماد بازار	BTCIRT
resolution	string	الزامی	بازه زمانی هر کندل	D
to	int	الزامی	زمان پایان بازه	1562230967
from	int	اختیاری	زمان ابتدای بازه	1562058167
countback	int	اختیاری	تعداد کندل‌های پیش از زمان پایان
(اولویت آن از from بیشتر است)	4
page	int	1	شماره صفحه	3
در صورت ورودی اشتباه برای resolution پاسخ به این صورت خواهد بود:

{
  "s": "error",
  "errmsg": "Invalid resolution!"
}
پارامتر resolution بازه زمانی کندل‌های خروجی می‌باشد و مقدار آن می‌تواند یکی از مقادیر زیر باشد:
دقیقه‌ای	توضیح	ساعتی	توضیح	روزانه	توضیح
1	یک دقیقه	60	یک ساعت	D	یک روز
5	پنج دقیقه	180	سه ساعت	2D	دو روز
15	یک ربع	240	چهار ساعت	3D	سه روز
30	نیم ساعت	360	شش ساعت		
720	دوازده ساعت		
مقادیر from و to زمان شروع و پایان جست‌وجو را مشخص می‌کند و با فرمت یونیکس به ثانیه مشخص می‌شود.
در صورت نبودن داده در بازه درخواستی پاسخ به این صورت خواهد بود:

{
  "s": "no_data"
}
 کندل‌های دقیقه‌ای بازارها از آغاز سال 1401 در دسترسند و دسترسی به کندل‌های دقیقه‌ای پیش از آن موجود نیست.
 لیست نمادهای معتبر بازارها عبارتند از:
BTCIRT, ETHIRT, LTCIRT, USDTIRT, XRPIRT, BCHIRT, BNBIRT, EOSIRT, XLMIRT, ETCIRT, TRXIRT, DOGEIRT, UNIIRT, DAIIRT, LINKIRT, DOTIRT, AAVEIRT, ADAIRT, SHIBIRT, FTMIRT, MATICIRT, AXSIRT, MANAIRT, SANDIRT, AVAXIRT, MKRIRT, GMTIRT, USDCIRT, BTCUSDT, ETHUSDT, LTCUSDT, XRPUSDT, BCHUSDT, BNBUSDT, EOSUSDT, XLMUSDT, ETCUSDT, TRXUSDT, PMNUSDT, DOGEUSDT, UNIUSDT, DAIUSDT, LINKUSDT, DOTUSDT, AAVEUSDT, ADAUSDT, SHIBUSDT, FTMUSDT, MATICUSDT, AXSUSDT, MANAUSDT, SANDUSDT, AVAXUSDT, MKRUSDT, GMTUSDT, USDCUSDT, CHZIRT, GRTIRT, CRVIRT, BANDUSDT, COMPUSDT, EGLDIRT, HBARUSDT, GALIRT, HBARIRT, WBTCUSDT, IMXIRT, WBTCIRT, ONEIRT, GLMUSDT, ENSIRT, 1M_BTTIRT, SUSHIIRT, LDOIRT, ATOMUSDT, ZROIRT, STORJIRT, ANTIRT, AEVOUSDT, 100K_FLOKIIRT, RSRUSDT, API3USDT, GLMIRT, XMRIRT, ENSUSDT, OMIRT, RDNTIRT, MAGICUSDT, TIRT, ATOMIRT, NOTIRT, CVXIRT, XTZIRT, FILIRT, UMAIRT, 1B_BABYDOGEIRT, BANDIRT, SSVIRT, DAOIRT, BLURIRT, ONEUSDT, EGALAUSDT, GMXIRT, XTZUSDT, FLOWUSDT, GALUSDT, WIRT, CVCUSDT, NMRUSDT, SKLIRT, SNTIRT, BATUSDT, TRBUSDT, NMRIRT, RDNTUSDT, API3IRT, CVCIRT, WLDIRT, YFIUSDT, SOLIRT, TUSDT, QNTUSDT, IMXUSDT, AEVOIRT, GMXUSDT, ETHFIUSDT, QNTIRT, GRTUSDT, WLDUSDT, FETIRT, AGIXIRT, NOTUSDT, LPTIRT, SLPIRT, MEMEUSDT, SOLUSDT, BALUSDT, DAOUSDT, COMPIRT, MEMEIRT, TONUSDT, BATIRT, SNXIRT, TRBIRT, 1INCHUSDT, OMUSDT, RSRIRT, RNDRIRT, SLPUSDT, SSVUSDT, RNDRUSDT, AGLDIRT, NEARUSDT, WOOUSDT, YFIIRT, MDTIRT, CRVUSDT, MDTUSDT, EGLDUSDT, LRCIRT, LPTUSDT, BICOUSDT, 1M_PEPEIRT, BICOIRT, MAGICIRT, ETHFIIRT, ANTUSDT, 1INCHIRT, APEUSDT, 1M_NFTIRT, ARBIRT, LRCUSDT, WUSDT, BLURUSDT, CELRUSDT, DYDXIRT, CVXUSDT, BALIRT, TONIRT, 100K_FLOKIUSDT, JSTUSDT, ZROUSDT, ARBUSDT, APTIRT, 1M_NFTUSDT, CELRIRT, UMAUSDT, SKLUSDT, ZRXUSDT, AGLDUSDT, ALGOIRT, NEARIRT, APTUSDT, ZRXIRT, SUSHIUSDT, FETUSDT, ALGOUSDT, 1M_PEPEUSDT, MASKIRT, EGALAIRT, FLOWIRT, 1B_BABYDOGEUSDT, MASKUSDT, 1M_BTTUSDT, STORJUSDT, XMRUSDT, OMGIRT, SNTUSDT, APEIRT, FILUSDT, ENJUSDT, OMGUSDT, WOOIRT, CHZUSDT, ENJIRT, DYDXUSDT, AGIXUSDT, JSTIRT, LDOUSDT, SNXUSDT
پارامترهای پاسخ
در هر درخواست بسته به پارامتر countback یا بازه زمانی تعیین شده و resolution انتخابی، تعداد کندل‌های برگشتی متفاوت است. برای مثال تعداد کندل‌های 1 ساعته از تاریخ 2019/2/9 15:39:41 تا چهار ساعت قبل آن، ۴ تاست.

پارامتر	توضیح	نوع	نمونه
s	وضعیت پاسخ	string	ok
t	شروع زمان	[ ] int	[1562182200]
o	قیمت شروع	[ ] float	[150551000]
h	بیشترین قیمت	[ ] float	[161869500]
l	کمترین قیمت	[ ] float	[150551000]
c	قیمت پایانی	[ ] float	[157000000]
v	حجم معاملات	[ ] float	[9.8592626506]
در هر درخواست حداکثر 500 کندل بازگردانده می‌شود. برای بازیابی همه کندل‌های یک بازه با بیش از 500 کندل، از پارامتر page برای صفحه‌بندی استفاده نمایید.



NEW API Mode

دریافت داده‌های OHLC
GET
https://apiv2.nobitex.ir/market/udf/history
داده‌های کندل (Open, High, Low, Close, Volume) را در قالب سازگار با TradingView UDF برمی‌گرداند.

در هر درخواست حداکثر ۵۰۰ کندل برگردانده می‌شود. برای بازه‌های بزرگ‌تر از پارامتر page استفاده کنید. کندل‌های دقیقه‌ای از آغاز سال ۱۴۰۱ در دسترس هستند.

این API عمومی است و به توکن نیاز ندارد. محدودیت فراخوانی آن ۶۰ درخواست در دقیقه است.

Request
Query Parameters
symbol
string
required
نماد بازار، مانند BTCIRT یا BTCUSDT.

Example: BTCIRT
resolution
string
required
Possible values: [1, 5, 15, 30, 60, 180, 240, 360, 720, D, 1D, 2D, 3D]

تایم‌فریم کندل: 1، 5، 15 و 30 دقیقه؛ 60، 180، 240، 360 و 720 دقیقه؛ و D یا 1D، 2D و 3D روز.

Example: D
from
int64
زمان شروع به صورت timestamp ثانیه.

Example: 1562058167
to
int64
required
زمان پایان به صورت timestamp ثانیه.

Example: 1562230967
countback
integer
تعداد کندل‌های درخواستی پیش از زمان to. در صورت ارسال، بر پارامتر from اولویت دارد و مقادیر بزرگ‌تر از ۵۰۰ به ۵۰۰ محدود می‌شوند.

Example: 4
page
integer
شماره صفحه برای دریافت دسته‌های قدیمی‌تر کندل‌ها.

Default value: 1
Example: 3
Header Parameters
User-Agent
string
برای شناسایی بات، این هدر را در همه درخواست‌های HTTP بات با الگوی TraderBot/<name-and-version> ارسال کنید. این هدر هنگام ورود خودکار با captcha=api الزامی و در سایر فراخوانی‌های بات اکیداً توصیه می‌شود.

Example: TraderBot/MyBot-1.0.0
Responses
200
400
موفق، بدون داده یا خطای UDF

application/json
Schema
Example (auto)
success
noData
invalidResolution
Schema
s
string
Possible values: [ok, no_data, error]

Example:
ok
t
int64[]
Possible values: <= 500

o
number[]
Possible values: <= 500

h
number[]
Possible values: <= 500

l
number[]
Possible values: <= 500

c
number[]
Possible values: <= 500

v
number[]
Possible values: <= 500

errmsg
string
پیام خطا در حالت s=error.

python
curl
go
java
javascript
HTTP.CLIENT
REQUESTS
import requests

url = "https://apiv2.nobitex.ir/market/udf/history?symbol=symbol&resolution=720&to=10"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)



