from paddleocr import draw_ocr
from PIL import Image

class ResultShower:
    def __init__(self) :
        pass

    def show_result(self, result):
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)
    
class ResultProcessor:
    def __init__(self, result):
        self.result = result  # 存储传入的数据

    def save_img(self, img_path, img_save_path):
        result = self.result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save(img_save_path)
    
    def save_result(self, file_path):
        with open(file_path, 'w',encoding='utf-8') as file:
            for item in self.result:
                 file.write(str(item) + '\n') 

    def find_subsequence_in_result(self, target):
        for item in self.result:
            pos = -1
            for lines in item:
                pos = pos + 1
                data = lines[1]
                text = data[0]  # 提取元组的第一个字符串（如 "苏HR"）
                if target in text:  # 检查 target 是否是 text 的子串
                    return pos , lines
        return None  # 如果没有找到，返回 None

    
    def find_midpos_in_result(self, pos):
        found_item = self.result[0][pos]
        mid_x = ( found_item[0][0][0] + found_item[0][1][0] ) / 2
        mid_y = ( found_item[0][0][1] + found_item[0][2][1] ) / 2
        return (mid_x, mid_y)
    

