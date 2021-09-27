# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

import PIL.Image as Image
import cv2

from qgui import CreateQGUI
from qgui.bar_tools import GitHub
from qgui.notebook_tools import ChooseFileTextButton, ChooseDirTextButton, RunButton, \
    RadioObviousToolButton, BaseButton, HorizontalToolsCombine
from qgui import MessageBox, show_file_or_path

from inference import main as infer_main


def infer(args):
    img_path = args["文件输入框"].get()
    out_path = args["保存位置"].get()
    mode = args["运行模式"].get()

    # 简单做个判断，保证输入是正确的
    if not os.path.exists(img_path):
        MessageBox.info("请选择要处理的图片")
        # 不选择就不做预测了
        return 1
    if not os.path.exists(out_path):
        MessageBox.info("请选择图片保存目录")
        return 2

    # 执行操作
    print("开始制作，请耐心等待...")
    if mode == "仅图像":
        file_ext = ".jpg"
        im = infer_main(img_path, "paint_best.pdparams", out_path, resize_h=512, resize_w=512)
    elif mode == "图像->视频":
        file_ext = ".mp4"
        im = infer_main(img_path, "paint_best.pdparams", out_path, resize_h=512, resize_w=512, serial=True,
                        need_animation=True)
    else:
        file_ext = ".mp4"
        im = infer_main(img_path, "paint_best.pdparams", out_path, resize_h=512, resize_w=512, video=True)

    im = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

    print("处理完毕，静态预览效果如下：")
    main_gui.print_image(im)
    button = HorizontalToolsCombine(tools=[BaseButton(bind_func=show_file_or_path(path=out_path),
                                                      text="打开文件所在的文件夹"),
                                           BaseButton(bind_func=
                                                      show_file_or_path(path=os.path.join(out_path,
                                                                                          "out_" +
                                                                                          os.path.splitext(
                                                                                              os.path.basename(
                                                                                                  img_path))[0] +
                                                                                          file_ext)),
                                                      text="打开文件")])
    main_gui.print_tool(button)


def bind_dir(args):
    img_path = args["文件输入框"].get()
    args["保存位置"].set(os.path.dirname(img_path))

    if os.path.splitext(img_path)[-1] == ".mp4":
        args["运行模式"].set("MP4视频->视频")
    else:
        print("选定的图片为")
        main_gui.print_image(img_path)


# 创建主界面
main_gui = CreateQGUI(title="Paint Master - 油画带师")

# 在界面最上方添加一个按钮，链接到GitHub主页
main_gui.add_banner_tool(GitHub("https://github.com/AP-Kai/Paint-Master"))
# 在主界面部分添加一个文件选择工具
main_gui.add_notebook_tool(ChooseFileTextButton(name="文件输入框", bind_func=bind_dir))
# 再加个文件夹选择工具
main_gui.add_notebook_tool(ChooseDirTextButton(name="保存位置"))
#
main_gui.add_notebook_tool(RadioObviousToolButton(["仅图像", "图像->视频", "MP4视频->视频"], name="运行模式", title="选择运行模式"))
# 添加一个运行按钮
main_gui.add_notebook_tool(RunButton(infer))
main_gui.set_navigation_info("项目介绍", "本项目基于PaddlePaddle和QGUI开发，主要功能为：图像油画化。\n"
                                     "稍作等待便可以得到一张笔底春风、笔精墨妙、笔墨横姿、不拘绳墨、丹青不渝、丹青妙手、画中有诗、挥翰成风、"
                                     "挥毫落纸、挥洒自如、活色生香、山节藻棁、山耶云耶、涉笔成趣、铁画银钩、下笔风雷、一挥而就的一张惟妙惟肖的"
                                     "油画。并且，您可以直观的感受到AI一步步生成油画的过程，很休闲，很是解压！")
# 简单加个简介
main_gui.set_navigation_about(author="AP-Kai",
                              version="0.0.1",
                              github_url="https://github.com/AP-Kai/Paint-Master")
# 跑起来~
main_gui.run()
