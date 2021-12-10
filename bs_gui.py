import time
import tkinter
from tkinter import ttk
import uuid
import requests
from io import BytesIO
import base64
import json
import threading
from tkinter.messagebox import showinfo, showerror
import traceback
import datetime

import cv2
import qrcode
from ttkbootstrap import Style
from PIL import Image, ImageTk, ImageDraw, ImageFont

from inference.inference import main as infer_main

SCALE = 1
font = ImageFont.truetype('LXGWWenKai-Bold.ttf', 35)
font2 = ImageFont.truetype('LXGWWenKai-Bold.ttf', 20)


def make_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return img


class LeftWin:
    def __init__(self, master):
        self.frame = ttk.Frame(master=master)

        im = Image.open("./resources/1.jpg")
        im = im.resize((int(1080 * SCALE), int(1080 * SCALE)))
        self.p = ImageTk.PhotoImage(im)
        self.show_img = ttk.Label(master=self.frame, image=self.p)
        self.show_img.pack(side="top", fill="x")
        self.frame.pack(side="left")


class RightWin:
    def __init__(self, master, left: LeftWin):
        # UUID
        self.now_uuid = None
        self.now_im = None
        self.left = left

        self.frame = ttk.Frame(master=master)

        self.top_f = ttk.Frame(master=self.frame)

        # 上部分
        im = Image.new(mode="RGB", size=(int(620 * SCALE), int(700 * SCALE)), color=(255, 255, 255))
        self.im = ImageTk.PhotoImage(im)
        self.top_f_im = ttk.Label(master=self.top_f, image=self.im)
        self.top_f_im.pack(side="top")

        # 启动按钮
        self.btn = ttk.Button(master=self.frame, text="启动服务", command=self.sync_run)
        self.btn.pack(anchor="se")

        self.top_f.pack(side="top")

        self.frame.pack(side="top")
        # self.set_next_qr()

    def sync_run(self):
        try:
            t = threading.Thread(target=self.maker)
            t.setDaemon(True)
            t.start()
            showinfo("提示", message="运行成功")
        except:
            traceback.print_exc()
            showerror("提示", message="运行失败，原因如下：\n" + str(traceback.format_exc()))

    def maker(self):
        while True:
            # 设置二维码
            self.set_next_qr()
            # 等待扫码
            while True:
                print(f"1| {datetime.datetime.now()} |检测扫码")
                act = requests.get(url="http://180.76.179.211:8004/api/check", params={"timestamp": self.now_uuid})
                act = act.json()
                if act["status"] == "success":
                    print(f"2| {datetime.datetime.now()} |检测成功")
                    link = act["link"]
                    f = requests.get(url=link, params={"timestamp": "xxxx"})

                    with open("./cache.jpg", "wb") as im_f:
                        im_f.write(f.content)
                    break
                else:
                    print(f"3| {datetime.datetime.now()} |尚未扫码")
                    time.sleep(1)

            """请求到图片后开始制作"""
            # 暂停二维码
            print(f"4| {datetime.datetime.now()} |暂停二维码")
            self.set_act()
            print(f"5| {datetime.datetime.now()} |开始推理")
            im = infer_main("./cache.jpg", "inference/paint_best.pdparams", "./cache_dir", resize_h=512, resize_w=512)
            # 展示图片
            im = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            im = im.resize((int(1080 * SCALE), int(1080 * SCALE)))
            # 添加下载二维码
            output_buffer = BytesIO()
            im.save(output_buffer, format='JPEG')
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data).decode(encoding="utf-8")
            print(f"6| {datetime.datetime.now()} |上传图片")
            requests.post(url="http://180.76.179.211:8004/api/upload_image",
                          params={"timestamp": self.now_uuid + "_dn"},
                          data=json.dumps({"image": base64_str}))

            print(f"http://180.76.179.211:8004/file/upload/{self.now_uuid}_dn.jpg")
            qr = make_qr(f"http://180.76.179.211:8004/file/upload/{self.now_uuid}_dn.jpg")
            qr = qr.resize((100, 100))
            # im.paste(qr, (10, 1500, 310, 1800))
            im.paste(qr, (10, 10, 110, 110))
            # 设置图片
            print(f"7| {datetime.datetime.now()} |设置图片")
            self.left.p = ImageTk.PhotoImage(im)
            self.left.show_img.configure(image=self.left.p)

    def set_next_qr(self):
        guid = uuid.uuid4()
        im = Image.new(mode="RGB", size=(600, 1000), color=(255, 255, 255))
        qr = make_qr("http://180.76.179.211:8004/web_upload_image?timestamp=" + str(guid))
        qr = qr.resize((600, 600))
        im.paste(qr, (0, 100, 600, 700))

        image_draw = ImageDraw.Draw(im)
        image_draw.text(xy=(30, 700),
                        text="手机扫码即可在线生成 油画风图像",
                        font=font,
                        fill=(0, 0, 0))

        self.now_im = im
        self.now_uuid = str(guid)
        self.im = ImageTk.PhotoImage(im)
        self.top_f_im.configure(image=self.im)

    def set_act(self):
        im = self.now_im

        mask = Image.new(mode="RGB", size=(300, 300), color=(255, 255, 255))
        image_draw = ImageDraw.Draw(mask)
        image_draw.text(xy=(20, 130),
                        text="正在制作，稍后将在左侧展示",
                        font=font2,
                        fill=(0, 0, 0))
        im.paste(mask, (150, 100 + 150, 150 + 300, 150 + 100 + 300))
        self.now_im = im
        self.im = ImageTk.PhotoImage(im)
        self.top_f_im.configure(image=self.im)


class MainGUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.style = Style("lumen")
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        global SCALE
        SCALE = self.h / 1080

        self.root.geometry("%dx%d" % (self.w, self.h))
        self.root.attributes("-topmost", True)
        self.root.title("油画大师 - https://github.com/AP-Kai/Paint-Master")

    def run(self):
        self.build()
        showinfo("提示", "请点击右上角启动服务进行启动")
        self.root.mainloop()

    def build(self):
        self.lw = LeftWin(self.root)
        self.rw = RightWin(self.root, self.lw)


if __name__ == '__main__':
    _m = MainGUI()
    _m.run()
