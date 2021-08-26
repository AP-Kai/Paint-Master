# Paint-Master 油画带师

基于Wechaty和PaintTransformer的图像油画带师。油画中的世界，美不胜收。



## 1.1 效果展示

视频链接：

GitHub链接：

## 1.2 项目介绍

本项目基于PaddlePaddle和Wechaty开发，主要功能为：图像油画化。您仅需向Robot发送一张图片，稍作等待便可以得到一张笔底春风、笔精墨妙、笔墨横姿、不拘绳墨、丹青不渝、丹青妙手、画中有诗、挥翰成风、挥毫落纸、挥洒自如、活色生香、山节藻棁、山耶云耶、涉笔成趣、铁画银钩、下笔风雷、一挥而就的一张惟妙惟肖的油画。并且，您可以直观的感受到AI一步步生成油画的过程，很休闲，很解压！

## 1.3 功能展示

### 1.3.1 图片油画化

功能入口：发送一张图片

![gif](https://user-images.githubusercontent.com/77101860/130989794-59ca6b63-7cd9-478a-8b4b-9cc0117a1038.gif)

## 1.4 Wechaty部分代码

```Python
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
    #调用inference method
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
```

## 1.5 参考项目

包括但不仅限于以下项目：

[PaintTransformer](https://github.com/wzmsltw/PaintTransformer)

[教你用AI Studio+wechaty+阿里云白嫖一个智能微信机器人](https://aistudio.baidu.com/aistudio/projectdetail/1836012?channelType=0&channel=0)

## 1.6 致谢

团队： 吃饱就睡队

成员： [AP-Kai](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/675310)、[nian53321](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/724244)

致谢：[PaintTransformer](https://github.com/wzmsltw/PaintTransformer)

​			感谢各位大佬的鼎力相助！

​			感谢飞桨！~~~



