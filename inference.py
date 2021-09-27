import numpy as np
from PIL import Image
import network
import os
import math
import render_utils
import paddle
import paddle.nn as nn
import paddle.nn.functional as F
import cv2
import render_parallel
import render_serial


def main(input_path,
         model_path,
         output_dir,
         need_animation=False,
         resize_h=None,
         resize_w=None,
         serial=False,
         brush=None,
         video=False):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    input_name = os.path.basename(input_path)
    output_path = os.path.join(output_dir, "out_" + os.path.splitext(input_name)[0])
    frame_dir = None
    if need_animation:
        if not serial:
            print('It must be under serial mode if animation results are required, so serial flag is set to True!')
            serial = True
        frame_dir = os.path.join(output_dir, input_name[:input_name.find('.')])
        if not os.path.exists(frame_dir):
            os.mkdir(frame_dir)
    stroke_num = 8

    # * ----- load model ----- *#
    net_g = network.Painter(5, stroke_num, 256, 8, 3, 3)
    net_g.set_state_dict(paddle.load(model_path))
    net_g.eval()
    for param in net_g.parameters():
        param.stop_gradient = True

    # * ----- load brush ----- *#
    brush_large_vertical = render_utils.read_img('brush/brush_large_vertical.png', 'L')
    brush_large_horizontal = render_utils.read_img('brush/brush_large_horizontal.png', 'L')
    meta_brushes = paddle.concat([brush_large_vertical, brush_large_horizontal], axis=0)

    import time
    t0 = time.time()
    if serial:
        original_img = render_utils.read_img(input_path, 'RGB', resize_h, resize_w)
        final_result_list = render_serial.render_serial(original_img, net_g, meta_brushes)
        if need_animation:
            print("total frame:", len(final_result_list))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path + ".mp4", fourcc, 20.0, (resize_h, resize_w))
            for idx, frame in enumerate(final_result_list):
                out.write(frame)
            else:
                return final_result_list[-1]
        else:
            cv2.imwrite(output_path, final_result_list[-1])
    elif video:
        tmp_path = os.path.join(output_dir, "cache")
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        cap = cv2.VideoCapture(input_path)
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path + ".mp4", fourcc, 20.0, (resize_h, resize_w))

        step = 0
        first_frame = None
        while cap.isOpened():
            ret, frame = cap.read()
            step += 1
            if ret is True:
                if step == 1:
                    print("正在处理首帧")
                    first_frame = frame
                    frame_path = os.path.join(tmp_path, "cache.jpg")
                    cv2.imwrite(frame_path, frame)
                    original_img = render_utils.read_img(frame_path, 'RGB', resize_h, resize_w)
                    final_result_list = render_serial.render_serial(original_img, net_g, meta_brushes)
                    for idx, frame in enumerate(final_result_list):
                        print("正在绘制", idx, "粒度的图像")
                        out.write(frame)
                    continue
                if step % 2 == 1:
                    print("正在处理", step // 2 + 1, "帧")
                    frame_path = os.path.join(tmp_path, "cache.jpg")
                    cv2.imwrite(frame_path, frame)
                    original_img = render_utils.read_img(frame_path, 'RGB', resize_h, resize_w)
                    final_result = render_parallel.render_parallel(original_img, net_g, meta_brushes)
                    for i in range(10):
                        out.write(final_result)
            else:
                break

        cap.release()
        out.release()
        return first_frame

    else:
        original_img = render_utils.read_img(input_path, 'RGB', resize_h, resize_w)
        final_result = render_parallel.render_parallel(original_img, net_g, meta_brushes)
        cv2.imwrite(output_path + ".jpg", final_result)
        return final_result

    print("total infer time:", time.time() - t0)


if __name__ == '__main__':
    main(input_path='image/925915968153427249.jpg',
         model_path='paint_best.pdparams',
         output_dir='./image/out/',
         need_animation=True,  # whether need intermediate results for animation.
         resize_h=512,  # resize original input to this size. None means do not resize.
         resize_w=512,  # resize original input to this size. None means do not resize.
         serial=True)  # if need animation, serial must be True.
