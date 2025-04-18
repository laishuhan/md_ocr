from paddleocr import PaddleOCR, draw_ocr
from module_ocr import ResultProcessor
from module_ocr import ResultShower
from path import img_path, save_result_path ,img_save_path
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
result = ocr.ocr(img_path, cls=True)

processor = ResultProcessor(result)

processor.save_img(img_path, img_save_path)

def find_idx_in_ans(idx,ans):
    target_idx = idx #"ALB"
    target_ans = ans #"结果"
    found_pos_idx, found_item_idx = processor.find_subsequence_in_result(target_idx)
    found_pos_ans, found_item_ans = processor.find_subsequence_in_result(target_ans)

    if found_item_idx:
        pass #print(f"找到的指标: {found_pos_idx , found_item_idx}")
    else:
        return -1 #print("没有找到目标指标")

    if found_item_ans:
        pass #print(f"找到的结果列: {found_pos_ans , found_item_ans}")
    else:
        return -2 #print("没有找到目标结果列")

    mid_x_idx, mid_y_idx = processor.find_midpos_in_result(found_pos_idx)#指标
    mid_x_ans, mid_y_ans = processor.find_midpos_in_result(found_pos_ans)#“结果”

    #------------------------------------------------------------------------
    #找到idx的一行

    i = 0
    t = result[0][found_pos_idx]
    tolerance = abs(t[0][1][1] - t[0][2][1]) / 2
    similar_items = []
    for items in result[0]:
        mid_x, mid_y = processor.find_midpos_in_result(i)
        if (abs(mid_y - mid_y_idx) <= tolerance and i != found_pos_idx):
                similar_items.append(i)
        i = i + 1

    similar_pos_x = []
    for pos in similar_items:
        mid_x, mid_y = processor.find_midpos_in_result(pos)
        similar_pos_x.append((pos, mid_x))

    #------------------------------------------------------------------------
    #找到与ans的一列的交点

    final_pos = -1
    dt = float('inf')

    for items in similar_pos_x:
        pos = items[0]
        num_x = items[1]
        if(abs(num_x - mid_x_ans) < dt):
            dt = abs(num_x - mid_x_ans)
            final_pos = pos

    if final_pos != -1:
        return final_pos #print(f"找到的指标结果: {result[0][final_pos]}")
    else:
        return -3 #print("没有找到目标指标的结果")

find_pos = find_idx_in_ans("巧克力豆", "生产车间")
print(result[0][find_pos])


     
    
    
    







