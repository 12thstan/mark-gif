# 工程：test
# 创建时间：2024/6/24 23:20
# encoding:utf-8

from PIL import Image, ImageDraw, ImageFont
import os
import configparser


def read_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)

    # 获取ini
    watermark_text = config['diy']['text']
    font_path = config['diy']['path']
    font_color = tuple(map(int, config['diy']['color'].split(',')))
    font_size = int(config['diy']['size'])
    position = tuple(map(int, config['diy']['xy'].split(',')))
    output = config['diy']['out']

    return watermark_text, font_path, font_color, font_size, position, output


def add_watermark_to_gif(gif_path, watermark_text, output_path, font_path, font_color, font_size, position):
    # 打开GIF图像
    with Image.open(gif_path) as gif:
        # 检查图像是否为GIF动画
        if gif.is_animated:
            # 获取GIF的帧数和持续时间
            frames = []
            durations = []
            for i in range(gif.n_frames):
                gif.seek(i)
                frame = gif.copy().convert("RGBA")  # 确保帧是RGBA模式
                frames.append(frame)
                durations.append(gif.info['duration'])

            # 为每一帧添加水印
            watermarked_frames = []
            for frame in frames:
                draw = ImageDraw.Draw(frame)
                # 加载字体
                font = ImageFont.truetype(font_path, font_size)

                # 在指定位置绘制水印
                draw.text(position, watermark_text, fill=font_color, font=font)
                watermarked_frames.append(frame)

            # 保存带有水印的GIF
            watermarked_gif = frames[0]
            watermarked_gif.save(
                output_path,
                save_all=True,
                append_images=watermarked_frames[1:],
                durations=durations,
                loop=0
            )
        else:
            # 如果GIF不是动画，只需为单帧添加水印
            with Image.open(gif_path) as img:
                img = img.convert("RGBA")  # 确保图像是RGBA模式
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(font_path, font_size)
                draw.text(position, watermark_text, fill=font_color, font=font)
                img.save(output_path)


def batch_add_watermark_to_gifs(gif_folder, ini_path):
    watermark_text, font_path, font_color, font_size, position, output = read_config(ini_path)

    # 确保输出文件夹存在
    if not os.path.exists(output):
        os.makedirs(output)

    # 遍历GIF文件夹中的所有文件
    for filename in os.listdir(gif_folder):
        if filename.lower().endswith(('.gif', '.webp')):
            input_path = os.path.join(gif_folder, filename)
            output_path = os.path.join(output, filename)
            add_watermark_to_gif(input_path, watermark_text, output_path, font_path, font_color, font_size, position)

        print(f"{filename}")

batch_add_watermark_to_gifs('input', 'user.ini')

print('图片已批量处理完成！')
