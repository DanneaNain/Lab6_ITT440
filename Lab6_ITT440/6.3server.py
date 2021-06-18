import socket
import sys
import time
import errno
import math
from multiprocessing import Process

OK_message = '\nHTTP/1.0 200 OKAY\n\n'
XOK_message = '\nHTTP/1.0 404 NOTFOUND!!\n\n'

def process_start(s_sock):
    s_sock.send(str.encode("\n\t\t Python's Online Calculator \n\nFunction Available : LOG(log), SQUARE ROOT(sqrt), EXPONENTIAL(exp) \n\n Calculation Step: log/sqrt/exp <number>  \n\nPlease type 'exit' to close"))
    while True:
        data = s_sock.recv(2048)
        data = data.decode("utf-8")

        try:
            operation, value = data.split()
            op = str(operation)
            num = int(value)

            if op[0] == 'l':
                op = 'Log'
                answer = math.log10(num)
            elif op[0] == 's':
                op = 'Square root'
                answer = math.sqrt(num)
            elif op[0] == 'e':
                op = 'Exponential'
                answer = math.exp(num)
            else:
                answer = ('Error !')

            sendAnswer = (str(op) + '(' + str(num) + ') = ' + str(answer))
            print ('Bravo! Your Calculation Successful !')
        except:
            print('OPSS, sorry :( Invalid input')
            sendAnswer ('OPS, sorry :( Invalid input')
        if not data:
            break

        s_sock.send(str.encode(sendAnswer))

    s_sock.close()

if __name__ == '__main__':
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.bind(("",8080))
      print("Waiting...")
      s.listen(28)

      try:
         while True:
            try:
                s_sock, s_addr = s.accept()
                p = Process(target=process_start, args=(s_sock,))
                p.start()

            except socket.error:

                print('socket error')

            except Exception as e:
                print("An exception has occured!")
                print(e)
                sys.exit(1)
      finally:
         s.close()
