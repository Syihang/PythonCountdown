# 倒计时程序 苏一行 20229639 2024/08/09
import tkinter as tk
from tkinter import messagebox
import winsound


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时程序")

        # 设置窗口居中
        self.center_window()

        # 声明部分变量
        self.hour_var = tk.StringVar()
        self.min_var = tk.StringVar()
        self.sec_var = tk.StringVar()

        self.create_widgets()
        self.running = False
        self.timer = None
        self.first_star = True

        self.total_seconds = 0

        # 添加Canvas和相关属性
        self.count = 0
        self.angle = 359.99
        self.cv = tk.Canvas(self.root, width=450, height=450, bg='white')
        self.cv.grid(row=4, column=0, columnspan=6, padx=10, pady=10)
        self.cv_arc = self.cv.create_oval(100, 50, 350, 300, fill='red', outline='yellow')
        self.cv.create_oval(150, 100, 300, 250, fill='yellow', outline='yellow')
        self.cv_text = self.cv.create_text(225, 175, text="00:00:00", font=('微软雅黑', 24, 'bold'), fill='red')

    # 设置窗口居中
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 470
        window_height = 500
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # 创建组件
    def create_widgets(self):
        tk.Label(self.root, text="设置时间:", font=("宋体", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="小时:", font=("宋体", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.hour_entry = tk.Entry(self.root, textvariable=self.hour_var, width=5, font=("微软雅黑", 12))
        self.hour_entry.grid(row=1, column=1, padx=10, pady=10)
        self.hour_var.set("0")

        tk.Label(self.root, text="分钟:", font=("宋体", 12)).grid(row=1, column=2, padx=10, pady=10)
        self.min_entry = tk.Entry(self.root, textvariable=self.min_var, width=5, font=("微软雅黑", 12))
        self.min_entry.grid(row=1, column=3, padx=10, pady=10)
        self.min_var.set("0")

        tk.Label(self.root, text="秒:", font=("宋体", 12)).grid(row=1, column=4, padx=10, pady=10)
        self.sec_entry = tk.Entry(self.root, textvariable=self.sec_var, width=5, font=("微软雅黑", 12))
        self.sec_entry.grid(row=1, column=5, padx=10, pady=10)
        self.sec_var.set("0")

        self.start_button = tk.Button(self.root, text="开始", command=self.start_countdown, font=("宋体", 12))
        self.start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.pause_button = tk.Button(self.root, text="暂停", command=self.pause_countdown, state=tk.DISABLED,
                                      font=("宋体", 12))
        self.pause_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.reset_button = tk.Button(self.root, text="重置", command=self.reset_countdown, font=("宋体", 12))
        self.reset_button.grid(row=2, column=4, columnspan=2, padx=10, pady=10)

    # 开始按钮
    def start_countdown(self):
        if self.first_star:
            try:
                h = int(self.hour_var.get()) if self.hour_var.get() else 0
                m = int(self.min_var.get()) if self.min_var.get() else 0
                s = int(self.sec_var.get()) if self.sec_var.get() else 0
            except ValueError:
                messagebox.showerror("错误", "请输入有效的时间")
                return

            self.total_seconds = h * 3600 + m * 60 + s

            if self.total_seconds > 0:

                self.hour_entry.config(state='disabled')
                self.min_entry.config(state='disabled')
                self.sec_entry.config(state='disabled')

                self.first_star = False
                self.running = True
                self.count = self.total_seconds
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                self.countdown()

            else:
                messagebox.showerror("错误", "输入时间必须为正值")
        else:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.countdown()

    # 暂停按钮
    def pause_countdown(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            if self.timer:
                self.timer.cancel()

    # 重置按钮
    def reset_countdown(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.hour_var.set("0")
        self.min_var.set("0")
        self.sec_var.set("0")

        self.hour_entry.config(state='normal')
        self.min_entry.config(state='normal')
        self.sec_entry.config(state='normal')

        self.reset_Canvas()
        self.angle = 359.99

    def countdown(self):
        if self.running and self.total_seconds > 0:
            h, m = divmod(self.total_seconds, 3600)
            m, s = divmod(m, 60)

            self.hour_var.set(str(h))
            self.min_var.set(str(m))
            self.sec_var.set(str(s))
            self.update_Canvas(f"{h:02d}:{m:02d}:{s:02d}")

            self.total_seconds -= 1

            self.root.after(1000, self.countdown)
        else:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            if self.total_seconds == 0:
                self.reset_countdown()
                # 清除并重新绘制弧形
                self.cv.delete(self.cv_arc)
                self.cv_arc = self.cv.create_arc(100, 50, 350, 300, start=90, extent=0, fill="red",outline='yellow')
                winsound.Beep(1000, 500)  # 频率1000Hz，持续500毫秒
                messagebox.showinfo("倒计时", "时间已到！")


    # 以下Canvas绘图模块参考自CSDN: Python动画制作：90秒倒计时圆形进度条效果(http://t.csdnimg.cn/LO2uz)
    def update_Canvas(self, time_str = "00:00:00"):

        if self.running:

            self.angle_step = 360 / self.count

            # 清除并重新绘制弧形
            if self.count == self.total_seconds:
                self.cv.delete(self.cv_arc)
                self.cv_arc = self.cv.create_arc(100, 50, 350, 300, start=90, extent=359.99, fill="red",outline='yellow')
            else:
                self.cv.delete(self.cv_arc)
                self.cv_arc = self.cv.create_arc(100, 50, 350, 300, start=90, extent=self.angle, fill="red", outline='yellow')

            self.angle -= self.angle_step

            # 绘制内部圆形和计数文本
            self.cv.create_oval(150, 100, 300, 250, fill='yellow', outline='yellow')
            self.cv.delete(self.cv_text)
            self.cv_text = self.cv.create_text(225, 175, text=time_str, font=('微软雅黑', 24, 'bold'), fill='red')

    def reset_Canvas(self):
        self.first_star = True

        # 清除并重新绘制弧形
        self.cv.delete("all")
        self.cv_arc = self.cv.create_arc(100, 50, 350, 300, start=90, extent=359.99, fill="red", outline='yellow')

        self.cv.create_oval(150, 100, 300, 250, fill='yellow', outline='yellow')
        self.cv_text = self.cv.create_text(225, 175, text="00:00:00", font=('微软雅黑', 24, 'bold'), fill='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

