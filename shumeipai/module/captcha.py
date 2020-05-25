import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class captcha:
    def __init__(self):
        self.font_path = 'msyhbd.ttc'  # 系统字体的位置
        self.number = 5  # 生成几位数的验证码
        self.size = (100, 30)  # 生成验证码图片的高度和宽度
        self.bgcolor = (255, 255, 255)  # 背景颜色，默认为白色
        self.fontcolor = (0, 0, 255)  # 字体颜色，默认为蓝色
        self.linecolor = (255, 0, 0)  # 干扰线颜色。默认为红色
        self.draw_line = True  # 是否要加入干扰线
        self.line_number = random.randint(3, 5)  # 加入干扰线条数,随机生成3-5之间的数

    #  随 机 生成一个字符串
    def gene_text(self):
        source = list(string.ascii_letters)
        for index in range(0, 10):
            source.append(str(index))
        return ''.join(random.sample(source, self.number))  # number是生成验证码的位数

    #  绘 制干扰线
    def gene_line(self, draw, width, height):
        for i in range(0, self.line_number):
            begin = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=self.linecolor)

    # 生 成 验证码
    def run(self):
        width, height = self.size  # 宽和高
        image = Image.new('RGBA', (width, height), self.bgcolor)  # 创建图片
        font = ImageFont.truetype(self.font_path, 25)  # 验证码的字体
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = self.gene_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / self.number, (height - font_height) / self.number), text,
                  font=font, fill=self.fontcolor)  # 填充字符串
        if self.draw_line:
            self.gene_line(draw, width, height)

        image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0),
                                Image.BILINEAR)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强

        # 保存验证码图片
        image.save('captcha.png')
        return text  # 返回生成验证码的字母，用于验证
