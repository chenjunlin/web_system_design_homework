from flask import Flask, request, render_template,redirect
import mysql.connector
from socket import *
conn=mysql.connector.connect(host='127.0.0.1',port=3306,user='root',passwd='password',db='order',charset='utf8')
cursor = conn.cursor()




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='chen' and password=='password':
         return redirect('http://127.0.0.1:5000/order')
    return render_template('form.html', message='用户名或密码错误', username=username)

@app.route('/order', methods=['GET'])
def order_form():
    return render_template('order_form.html')

@app.route('/noinfo', methods=['GET'])
def order_detail2():
    return render_template('noinfo.html')


@app.route('/order', methods=['POST'])
def order_consult():

    order_id = request.form['user'] 

    cursor.execute('select * from order_table where order_id = %s', (order_id,))
    values = cursor.fetchall()

    if len(values) == True:
        return render_template('order_detail.html',order_id = values[0][0],
            order_from = values[0][1],
            order_go = values[0][2],
            order_date = values[0][3],
            order_arrival_date = values[0][4],
            order_arrival = values[0][5])

    return redirect('http://127.0.0.1:5000/noinfo')




@app.route('/order_detail', methods=['GET'])
def order_detail1():
    return render_template('order_detail.html')

@app.route('/reserve', methods=['GET'])
def reserve():
    return render_template('reserve.html')

@app.route('/reserve', methods=['POST'])
def write_form():
    place_from = request.form['place_from']
    place_go = request.form['place_go']
    phone_from = request.form['phone_from']
    phone_go = request.form['phone_go']

    #检查用户输入值是否非空并向udp服务器发送数据
    if (phone_from and phone_go and place_from and place_go):
        cursor.execute('insert into order_table (order_from, order_go) values (%s, %s)', (place_from, place_go))
        conn.commit()

        host  = '192.168.1.2' 
        port = 13141 
        bufsize = 1024  #定义缓冲大小

        addr = (host,port) 
        udpClient = socket(AF_INET,SOCK_DGRAM) 

        data1=(place_from)
        data2=(phone_from)

        data1 = data1.encode(encoding="utf-8") 
        data2= data2.encode(encoding="utf-8") 
        udpClient.sendto(data1,addr) # 发送数据
        udpClient.sendto(data2,addr) # 发送数据


        return redirect('http://127.0.0.1:5000/reserve_done')

    return render_template('reserve.html', message='请补全信息')

@app.route('/reserve_done', methods=['GET'])
def order_done():
    
    cursor.execute('select max(order_id) from order_table;')
    order_id  = cursor.fetchall()
    number = order_id[0][0]



    return render_template('number.html',number=number)


if __name__ == '__main__':
    app.run()
