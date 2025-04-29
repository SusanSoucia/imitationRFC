import tkinter as tk
from tkinter import messagebox
import socket


def main():
    serverName = 'your server address'  # Replace with your server address
    serverPort = 2525
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((serverName, serverPort))
    except Exception as e:
        messagebox.showerror("连接错误", f"无法连接到服务器: {e}")
        return

    def validate_card():
        user_id = card_entry.get()
        card_number = "HELO " + user_id
        client_socket.send(card_number.encode())
        response = client_socket.recv(1024).decode()
        if response == "500 AUTH REQUIRE":
            root.destroy()
            open_pin_window()
        elif response == "401 ERROR!":
            messagebox.showerror("错误", "卡号无效")

    def open_pin_window():
        pin_window = tk.Tk()
        pin_window.geometry("400x250+600+300")
        pin_window.title("输入 PIN 码")
        tk.Label(pin_window, text="请输入 PIN 码:",font=("Arial", 12)).place(x=0, y=50, width=400, height=25)
        pin_entry = tk.Entry(pin_window, show="*")
        pin_entry.place(x=50, y=80, width=300, height=30)

        def validate_pin():
            input_pin = pin_entry.get()
            pin = "PASS " + input_pin
            client_socket.send(pin.encode())
            response = client_socket.recv(1024).decode()
            if response == "401 ERROR!":
                messagebox.showerror("错误", "密码错误！")
            elif response == "525 OK!":
                pin_window.destroy()
                open_operation_window()

        tk.Button(pin_window, text="确认", command=validate_pin,font=("Arial", 11)).place(x=175, y=140,width=60,height=30)

    def open_operation_window():
        operation_window = tk.Tk()
        operation_window.title("操作选择")
        operation_window.geometry("400x300+600+300")
        def query_balance():
            client_socket.send("BALA".encode())
            balance = client_socket.recv(1024).decode()
            messagebox.showinfo("余额查询", f"您的余额是: {balance[5:]}")

        def withdraw():
            def withdraw_money():
                amount = amount_entry.get()
                client_socket.send(f"WDRA {amount}".encode())
                response = client_socket.recv(1024).decode()
                if response == "401 ERROR!":
                    messagebox.showerror("错误", "余额不足")
                elif response == "525 OK!":
                    messagebox.showinfo("提示", "取款成功")
                withdraw_window.destroy()
            withdraw_window=tk.Tk()
            withdraw_window.geometry("300x200+650+350")
            tk.Label(withdraw_window, text="请输入取款金额:",font=("Arial", 12)).place(x=0, y=30, width=150, height=30)
            amount_entry = tk.Entry(withdraw_window)
            amount_entry.place(x=62, y=70, width=175, height=40)
            tk.Button(withdraw_window, text="确认", command=withdraw_money).place(x=115, y=140, width=70, height=30)


        def exit_app():
            def close_N():
                close_window.destroy()
            def close_Y():
                client_socket.send("BYE".encode())
                response = client_socket.recv(1024).decode()
                if response == "BYE":
                    close_window.destroy()
                    operation_window.destroy()
                    client_socket.close()
            close_window=tk.Tk()
            close_window.geometry("300x200+650+350")
            tk.Label(close_window, text="请确认是否退出!", font=("Arial", 15)).place(x=0, y=50, width=300, height=30)
            tk.Button(close_window, text="取消", command=close_N).place(x=70, y=120, width=50, height=30)
            tk.Button(close_window, text="确认", command=close_Y).place(x=180, y=120, width=50, height=30)

        tk.Label(operation_window, text="请选择想要进行的操作:",font=("Arial", 12)).place(x=0, y=30, width=180, height=30)
        tk.Button(operation_window, text="1.查询余额", command=query_balance,font=("Arial", 11)).place(x=160, y=90, width=100, height=30)
        tk.Button(operation_window, text="2.取款", command=withdraw,font=("Arial", 11)).place(x=160, y=140, width=100, height=30)
        tk.Button(operation_window, text="3.退出", command=exit_app,font=("Arial", 11)).place(x=160, y=190, width=100, height=30)

    root = tk.Tk()
    root.title("ATM 客户端")
    root.geometry("400x300+600+300")
    label1=tk.Label(root, text="ATM 客户端",font=("Arial", 15)).place(x=0,y=10,width=400,height=30)

    label2=tk.Label(root, text="请输入卡号:",font=("Arial", 12)).place(x=0,y=50,width=400,height=30)
    card_entry = tk.Entry(root)
    card_entry.place(x=50,y=85,width=300,height=30)
    tk.Button(root, text="确认", command=validate_card,font=("Arial", 11)).place(x=175,y=140,width=60,height=30)
    root.mainloop()


if __name__ == "__main__":
    main()
