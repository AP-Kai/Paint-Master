import os
import asyncio
from inference import main as infer
from PIL import Image
from image2gif import image2gif
from image2gif import image2mp4
from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

os.environ['WECHATY_PUPPET'] = "wechaty-puppet-service"
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = "puppet_padlocal_a48ae36edb074414a1db144d401ee05"  # 这里填Wechaty token
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


async def on_message(msg: Message):
    if msg.text() == 'ding':
        await msg.say('dong')

    if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        # 将Message转换为FileBox
        file_box = await msg.to_file_box()
        # 获取图片名
        img_name = file_box.name
        # 图片保存的路径
        img_path = './image/' + img_name
        print(img_path)
        # 将图片保存为本地文件
        await file_box.to_file(file_path=img_path)
        infer(input_path=img_path,
              model_path='paint_best.pdparams',
              output_dir='./image/out',
              need_animation=True,
              resize_h=512,
              resize_w=512,
              serial=True)
        image2mp4(img_name)
        file_box = FileBox.from_file('./image/out/' + img_name.split('.')[0] + '/' + 'result.mp4')
        await msg.say(file_box)


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
