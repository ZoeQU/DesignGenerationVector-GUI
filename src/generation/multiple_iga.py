# -*- coding:utf-8 -*-
import random
import math
import subprocess
from deap import base, creator, tools
from xml.dom import minidom
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def calculate_bounding_box(center_x, center_y, deviation, scale):
    """计算图案的边界框，考虑旋转后的最大范围"""
    scaled_deviation = deviation * abs(scale)
    return {
        "left": center_x - scaled_deviation,
        "right": center_x + scaled_deviation,
        "top": center_y - scaled_deviation,
        "bottom": center_y + scaled_deviation,
    }


def calculate_overlap_area(box1, box2):
    """计算两个边界框之间的重叠面积"""
    overlap_left = max(box1["left"], box2["left"])
    overlap_right = min(box1["right"], box2["right"])
    overlap_top = max(box1["top"], box2["top"])
    overlap_bottom = min(box1["bottom"], box2["bottom"])

    # 如果没有交集，返回重叠面积为 0
    if overlap_left >= overlap_right or overlap_top >= overlap_bottom:
        return 0

    # 计算交集面积
    overlap_width = overlap_right - overlap_left
    overlap_height = overlap_bottom - overlap_top
    return overlap_width * overlap_height


def is_overlap(new_box, existing_boxes):
    """检测新边界框是否与已有边界框重叠"""
    for box in existing_boxes:
        if calculate_overlap_area(new_box, box) > 0:
            return True  # 有重叠
    return False


def adjust_position_to_fit_bounds(cx, cy, deviation, scale, canvas_size):
    """调整图案位置，确保边界框在画布范围内"""
    scaled_deviation = deviation * abs(scale)

    # 确保边界框不会超出画布范围
    cx = max(scaled_deviation, min(cx, canvas_size - scaled_deviation))
    cy = max(scaled_deviation, min(cy, canvas_size - scaled_deviation))
    return cx, cy


def mutate_element(element, canvas_size, deviation):
    """对单个设计元素进行变异（cx, cy, scale, rotation）"""
    cx, cy, scale, rotation, index = element

    # 对每个参数进行随机变异
    cx += random.gauss(0, 10)  # 高斯变异
    cy += random.gauss(0, 10)
    scale += random.gauss(0, 0.1)
    rotation += random.gauss(0, 5)

    # 重新调整位置，确保不出画板
    cx, cy = adjust_position_to_fit_bounds(cx, cy, deviation, scale, canvas_size)

    # 确保 scale 在合理范围内
    scale = max(0.1, min(scale, 1))

    # 确保 rotation 在 0-360 度范围内
    rotation = rotation % 360

    return [cx, cy, scale, rotation, index]

class MultipleGA():
    def __init__(self, savename, design_elements):
        self.savename = savename
        self.design_elements = []
        self.n = len(design_elements)

        # 解析每个设计元素
        for element_path in design_elements:
            doc = minidom.parse(element_path)
            paths = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
            path_colors = [path.getAttribute('fill') for path in doc.getElementsByTagName('path')]
            bk_color = [rect.getAttribute('fill') for rect in doc.getElementsByTagName('rect')][0]
            width = int(float([rect.getAttribute('width') for rect in doc.getElementsByTagName('rect')][0]))
            height = int(float([rect.getAttribute('height') for rect in doc.getElementsByTagName('rect')][0]))

            # 计算 deviation，考虑旋转后的最大边界
            deviation = math.hypot(width / 2, height / 2)

            self.design_elements.append({
                "paths": paths,
                "path_colors": path_colors,
                "bk_color": bk_color,
                "width": width,
                "height": height,
                "deviation": deviation,
            })

        self.bk_color = bk_color
        self.rect_length = 4 * max(max(de['width'] for de in self.design_elements),
                                   max(de['height'] for de in self.design_elements))  # ori 2 times

        # 设置个体与种群
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.generate_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def custom_mutate(self, individual):
        """自定义变异函数"""
        for i, element in enumerate(individual):
            deviation = self.design_elements[element[4]]["deviation"]
            individual[i] = mutate_element(element, self.rect_length, deviation)
        return individual,

    def generate_individual(self):
        """生成一个包含所有设计元素的个体，并确保没有重叠"""
        individual = []
        existing_boxes = []

        for i, design_element in enumerate(self.design_elements):
            deviation = design_element["deviation"]

            # while True:
            #     # 随机生成 cx, cy，scale 和 rotation
            #     scale = random.uniform(0.3, 1)
            #     cx = random.uniform(0, self.rect_length)
            #     cy = random.uniform(0, self.rect_length)
            #     rotation = random.uniform(0, 360)

            #     # 调整位置，确保在画布范围内
            #     cx, cy = adjust_position_to_fit_bounds(cx, cy, deviation, scale, self.rect_length)

            #     # 计算边界框
            #     new_box = calculate_bounding_box(cx, cy, deviation, scale)

            #     # 检查是否与已有元素重叠
            #     if not is_overlap(new_box, existing_boxes):
            #         # 如果不重叠，添加到现有边界框列表，并存入个体
            #         existing_boxes.append(new_box)
            #         individual.append([cx, cy, scale, rotation, i])  # i 是 design element 的索引
            #         break

            # 每个设计元素复制两份
            for replication in range(2):  # 至少复制一份
                while True:
                    # 随机生成 cx, cy，scale 和 rotation
                    scale = random.uniform(0.3, 1)
                    cx = random.uniform(0, self.rect_length)
                    cy = random.uniform(0, self.rect_length)
                    rotation = random.uniform(0, 360)

                    # 调整位置，确保在画布范围内
                    cx, cy = adjust_position_to_fit_bounds(cx, cy, deviation, scale, self.rect_length)

                    # 计算边界框
                    new_box = calculate_bounding_box(cx, cy, deviation, scale)

                    # 检查是否与已有元素重叠
                    if not is_overlap(new_box, existing_boxes):
                        # 如果不重叠，添加到现有边界框列表，并存入个体
                        existing_boxes.append(new_box)
                        individual.append([cx, cy, scale, rotation, i])  # i 是 design element 的索引
                        break

        return creator.Individual(individual)

    def draw_pattern(self, individual):
        """绘制图案并保存为 SVG 文件，支持 t*t 的平铺"""
        t = 2
        # 设置整体 SVG 文件的宽高（每个单元的大小为 self.rect_length）
        svg_width = self.rect_length * t
        svg_height = self.rect_length * t

        # SVG 的头部信息
        svg_content = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" fill="{self.bk_color}">\n'
        )
        svg_content += f'<rect width="{svg_width}" height="{svg_height}" fill="{self.bk_color}"/>\n'

        # 遍历 t * t 网格
        for row in range(t):  # 控制行
            for col in range(t):  # 控制列
                # 当前单元格的偏移量
                x_offset = col * self.rect_length
                y_offset = row * self.rect_length

                # 遍历 individual 中的每个设计元素
                for cx, cy, scale, rotation, element_index in individual:
                    # 获取对应的设计元素
                    element = self.design_elements[element_index]
                    prop1 = 'transform="translate(0.0,0.0) scale(0.1,-0.1)" stroke="none"'

                    # 在当前单元格内绘制图案（加上偏移量）
                    for path, color in zip(element["paths"], element["path_colors"]):
                        svg_content += (
                            f'<g id="{row}_{col}" transform="translate({cx + x_offset},{cy + y_offset}) scale({scale}) rotate({rotation})">\n'
                        )
                        svg_content += f'<path d="{path}" {prop1} fill="{color}" />\n'
                        svg_content += '</g>\n'

        # 结束 SVG
        svg_content += '</svg>'

        # 保存到文件
        with open(self.savename, "w") as f:
            f.write(svg_content)

        # self.svg_visualization()
        print(f"Saved SVG to {self.savename}")


    def svg_visualization(self):
        # 临时 PNG 文件路径
        temp_png = self.savename.replace(".svg", ".png")

        # 使用 Inkscape 命令行导出 PNG
        command = [
            "inkscape",
            self.savename,
            "--export-png", temp_png,  # 导出为 PNG
            "--export-dpi", str(96),  # 设置分辨率
            "--export-area-drawing"   # 导出绘图区域
        ]
        subprocess.run(command, check=True)
        print(f"Successfully exported SVG to PNG: {temp_png}")

        img = mpimg.imread(temp_png)
        plt.imshow(img)
        plt.axis('off') 
        plt.show()


    def generate_pattern(self):
        """初始化种群和遗传算法设置"""
        # 注册遗传算法操作
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self.custom_mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # 初始化种群
        self.population = self.toolbox.population(n=10)
        self.current_generation = 0  # 当前代数
        print("Initialization complete. Starting generation process...")

        # 开始生成第一代图案
        svg_names = []
        candidates = []
        for i in range(6):  # 生成 6 个图案
            individual = random.choice(self.population)  # 从种群中随机选择个体
            svg_name = f"{self.savename.replace('.svg', '')}_gen_0_ind_{i}.svg"
            self.savename = svg_name
            self.draw_pattern(individual)  # 绘制图案并保存
            print(f"Generated {svg_name}")
            svg_names.append(svg_name)
            candidates.append(individual)

        # 保存第一代的候选个体
        self.candidates = candidates
        return svg_names

    # def generate_next_iteration(self):
    #     """生成下一代"""
    #     if self.current_generation >= 100:  # 达到最大代数时停止
    #         print("Reached maximum generations. Process finished.")
    #         return

    #     print(f"Generation {self.current_generation + 1}")

    #     # 从种群中随机选择一个个体，并绘制图案
    #     individual = random.choice(self.population)
    #     self.draw_pattern(individual)  # 绘制当前图案
    #     self.current_individual = individual  # 保存当前个体以备需要

    #     # 用户反馈逻辑改成由外部触发（例如通过按钮或事件）
    #     print("Waiting for user feedback...")  # 提示，需要由外部调用处理反馈

    #     # 将当前代数更新（不立即生成下一代，等待用户交互）
    #     self.current_generation += 1
    
    def generate_next_iteration(self, selected_indices):
        """生成下一代图案 (交互式遗传算法)"""
        if self.current_generation >= 100:  # 达到最大代数时停止
            print("Reached maximum generations. Process finished.")
            return

        print(f"Generation {self.current_generation + 1}")

        # Step 1: 从用户选择的索引中提取对应的个体
        selected_individuals = [self.candidates[idx] for idx in selected_indices]

        if not selected_individuals:
            print("No designs selected. Exiting...")
            return []

        # Step 2: 遗传操作（交叉和变异）
        offspring = []
        while len(offspring) < len(self.population):
            # 随机选择两个用户喜欢的个体进行交叉
            parent1, parent2 = random.sample(selected_individuals, 2)
            child1, child2 = self.toolbox.clone(parent1), self.toolbox.clone(parent2)

            # 交叉
            if random.random() < 0.5:  # 50% 交叉概率
                self.toolbox.mate(child1, child2)

            # 变异
            if random.random() < 0.2:  # 20% 变异概率
                self.toolbox.mutate(child1)
            if random.random() < 0.2:
                self.toolbox.mutate(child2)

            offspring.append(child1)
            if len(offspring) < len(self.population):
                offspring.append(child2)

        # Step 3: 更新种群并进入下一代
        self.population[:] = selected_individuals + offspring[:len(self.population) - len(selected_individuals)]
        self.current_generation += 1

        # Step 4: 生成下一代图案
        svg_names = []
        self.candidates = []
        for i in range(6):  # 生成 6 个图案
            individual = random.choice(self.population)  # 从种群中随机选择个体
            svg_name = f"{self.savename.replace('.svg', '')}_gen_{i}.svg"
            self.savename = svg_name
            self.draw_pattern(individual)  # 绘制图案并保存
            print(f"Generated {svg_name}")
            svg_names.append(svg_name)
            self.candidates.append(individual)

        print(f"Finished generation {self.current_generation}.")
        return svg_names


if __name__ == "__main__":
    design_elements = [
        "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/svg/test_filter_num_28.svg",
        "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/svg/test_rect_green.svg",
        "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/svg/test_rect_red.svg"
    ]
    svgname = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/temp_save/test.svg"
    multiple_ga = MultipleGA(svgname, design_elements)
    multiple_ga.generate_pattern()