import os
import numpy as np
import imageio
import cv2
from PIL import Image


def image2gif(img_name):
    # 需要合在一起的图片
    # image_list = [r'./image/output/' + img_name.split('.')[0]+'/'+ str(x) + ".png" for x in range(000, 170)]
    image_list = os.listdir('./image/out/' + img_name.split('.')[0]+'/')
    # gif的图片名
    gif_name = r'./image/out/' + img_name.split('.')[0] + '/' + img_name.split('.')[0] + '.gif'
    frames = []
    i = 0
    for image_name in image_list:
        if i % 1 == 0:
            image_name = './image/out/' + img_name.split('.')[0] + '/' + image_name
            frames.append(imageio.imread(image_name))
        i = i + 1
    # druation : 图片切换的时间，单位秒
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.08)
    print('image2gif success')


def image2mp4(img_name):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    files = os.listdir('./image/out/' + img_name.split('.')[0]+'/')
    img = Image.open('./image/' + img_name)  # 需要整合成视频的图片路径
    w = img.size[0]
    h = img.size[1]
    j = 0
    out = cv2.VideoWriter('./image/out/' + img_name.split('.')[0]+'/result.mp4', fourcc, 30, (img.size[0], img.size[1]))
    for i in files:
        if j % 2 == 0:
            img1 = cv2.imread('./image/out/' + img_name.split('.')[0]+'/' + i)
            img2 = cv2.resize(img1, (w, h), interpolation=cv2.INTER_NEAREST)
            out.write(img2)  # 保存帧
        j = j + 1
    out.release()
    print('ok!')


# image2gif('925915968153427249.jpg')