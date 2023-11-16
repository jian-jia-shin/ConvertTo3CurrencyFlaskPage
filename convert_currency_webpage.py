from flask import Flask, render_template, request
import requests

app = Flask(__name__)

r=requests.get('https://tw.rter.info/capi.php')
##  API來源 ： ©RTER.info 2023
currency=r.json()
USTW=currency['USDTWD']['Exrate']
USJP=currency['USDJPY']['Exrate']
USKR=currency['USDKRW']['Exrate']
getUptadeTime=currency['USDTWD']['UTC']

def convertToResult(MainCurrency,MainMoney,ConvertCurrency):
    MainCurrency_name = str(MainCurrency)
    getMainCurrency_Code=MainCurrency_name[len(MainCurrency_name)-4:len(MainCurrency_name)-1]
    ConvertCurrency_name = str(ConvertCurrency)
    getConvertCurrency_Code = ConvertCurrency_name[len(ConvertCurrency_name) - 4:len(ConvertCurrency_name) - 1]

    MainMoney = float(MainMoney)
    result=0.0
    if getMainCurrency_Code==getConvertCurrency_Code:
        result=MainMoney
    else:
        if getMainCurrency_Code=="USD" and getConvertCurrency_Code!="USD":
            convertCurCode="USD"+str(getConvertCurrency_Code)
            exrate = float(currency[convertCurCode]['Exrate'])
            result = float(MainMoney*exrate)
        if getMainCurrency_Code!="USD" and getConvertCurrency_Code=="USD":
            convertCurCode="USD"+str(getMainCurrency_Code)
            exrate = float(currency[convertCurCode]['Exrate'])
            result = float(MainMoney/exrate)
        if getMainCurrency_Code!="USD" and getConvertCurrency_Code!="USD":
            convertCurCode1 = "USD" + str(getMainCurrency_Code)
            convertCurCode2 = "USD" + str(getConvertCurrency_Code)
            exrate1 = float(currency[convertCurCode1]['Exrate'])
            exrate2 = float(currency[convertCurCode2]['Exrate'])
            result = float((MainMoney/exrate1)*exrate2)
    return result

@app.route('/ConvertTo3CurrencyPage', methods=['GET', 'POST'])
def index():
    options = ['美金 (USD)','歐元 (EUR)','日幣 (JPY)','港幣 (HKD)','英鎊 (GBP)',
                '瑞士法郎 (CHF)','人民幣 (CNY)','離岸人民幣 (CNH)','韓元 (KRW)',
                '澳幣 (AUD)','紐幣 (NZD)','新加坡幣 (SGD)','泰銖 (THB)',
                '瑞典幣 (SEK)','馬來幣 (MYR)','加拿大幣 (CAD)','越南盾 (VND)',
                '澳門幣 (MOP)','菲律賓比索 (PHP)','印度盧比 (INR)','印尼盾 (IDR)',
                '丹麥克朗 (DKK)','南非蘭特 (ZAR)','墨西哥披索 (MXN)',
                '土耳其里拉 (TRY)','台幣 (TWD)']

    if request.method == 'POST':
        # selected_optionMain = request.form.get('optionMain')
        # selected_option_convert1 = request.form.get('option_convert1')
        Maincurrency = request.form.get('optionMain')
        Convert1 = request.form.get('option_convert1')
        Convert2 = request.form.get('option_convert2')
        Convert3 = request.form.get('option_convert3')

        MainMoney_show = request.form.get('main_currency')

        try:
            Result1 = convertToResult(Maincurrency, MainMoney_show, Convert1)
            Result2 = convertToResult(Maincurrency, MainMoney_show, Convert2)
            Result3 = convertToResult(Maincurrency, MainMoney_show, Convert3)
            result_text = f"主要貨幣\"{Maincurrency}\"，金額是:{MainMoney_show}<br>換算結果:<br>(1)換成\"{Convert1}\"==>{format(Result1,'.2f')}<br>(2)換成\"{Convert2}\"==>{format(Result2,'.2f')}<br>(3)換成\"{Convert3}\"==>{format(Result3,'.2f')}<br><br>匯率更新時間:{getUptadeTime}"
        except:
            result_text = "出現錯誤"

        #result_text = f'OPTION1: {selected_optionMain}, OPTION2: {selected_option_convert1}, OPTION3: {selected_option_convert1}'
        return render_template('convert_currency_page.html', options=options, result_text=result_text)

    return render_template('convert_currency_page.html', options=options, result_text='')


if __name__ == '__main__':
    app.run(debug=False)
