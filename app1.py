from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyodbc
app = Flask(__name__)

VALID_USERNAME = 'siddharth'
VALID_PASSWORD = 'pass'


creds = ServiceAccountCredentials.from_json_keyfile_name('vertical-sunset-400909-16ac0f419f04.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(creds)
con = pyodbc.connect('DRIVER={SQL Server};Server=tcp:48hours.database.windows.net;Database=48hours;Port=1433;UID=messaging;Pwd=Test@123')
# sheet1 = client.open_by_key('1UQ87xCSp3Ao6QNR_YWlCyJK5XKf6q-mI7vhCfJXKOO8').sheet1
# values = sheet1.get_all_records()
# df = pd.DataFrame(values)
# df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
# sheet2 = client.open_by_key('11SRykmr3glZjT5XPnX4g90mm6k9yjNKqpnmPi8zMFNU').sheet1
# values1 = sheet2.get_all_records()
# df1 = pd.DataFrame(values1)
# df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')
# sheet3 = client.open_by_key('1lp1dgxSErmkS-Y9QQfuYGXW9niLFvAdVrl473pgcMGk').sheet1
# values2 = sheet3.get_all_records()
# df2 = pd.DataFrame(values2)
# df2['Date'] = pd.to_datetime(df2['Date']).dt.strftime('%Y-%m-%d')
# print(df2)
# sheet4 = client.open_by_key('10b2tg6eg85llcbM5pOMcnnYv4eFImM10pqVuDZ94e-8').sheet1
# values3 = sheet4.get_all_records()
# df3 = pd.DataFrame(values3)
#excel_file = 'exc1.xlsx'
#df = pd.read_excel(excel_file)
#df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
#excel_file1 = 'exc2.xlsx'
#df1 = pd.read_excel(excel_file1)
#df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')
@app.route('/', methods=['GET', 'POST'])
def index():
    q1="select * from dbo.BirthdayWishes"
    df=pd.read_sql(q1, con)
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    filtered_df = df[df['Email_Id_of_Recipient'].str.contains(VALID_USERNAME)]
    q2="select * from dbo.AppreciationsTable"
    df1=pd.read_sql(q2, con)
    df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')
    filtered_df1 = df1[df1['Email_Id_of_Recipient'].str.contains(VALID_USERNAME)]
    q3="select * from dbo.AnniversaryWishes"
    df2=pd.read_sql(q3, con)
    df2['Date'] = pd.to_datetime(df2['Date']).dt.strftime('%Y-%m-%d')
    filtered_df2 = df2[df2['Email_Id_of_Recipient'].str.contains(VALID_USERNAME)]
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            wishes_data = filtered_df[['Wish', 'Sender','Date']].to_dict(orient='records')
            appreciations_data = filtered_df1[['Reason', 'Sender','Date']].to_dict(orient='records')
            anniversary_data = filtered_df2[['Anniversary_Wish', 'Sender','Date']].to_dict(orient='records')
            return render_template('index.html', wishes_data=wishes_data, appreciations_data=appreciations_data, username=username,anniversary_data=anniversary_data)
        else:
            return redirect(url_for('login.html'))

    return render_template('login.html')
@app.route('/images')
def images():
    sheet4 = client.open_by_key('10b2tg6eg85llcbM5pOMcnnYv4eFImM10pqVuDZ94e-8').sheet1
    values3 = sheet4.get_all_records()
    df3 = pd.DataFrame(values3)
    return render_template('images.html',images_data=df3)
if __name__ == '__main__':
    app.run(debug=True)