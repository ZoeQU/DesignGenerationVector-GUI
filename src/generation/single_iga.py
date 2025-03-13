# -*- coding:utf-8 -*-
import random
import math
import subprocess
from deap import base, creator, tools
from xml.dom import minidom
import matplotlib.pyplot as plt
import matplotlib.image as mpimg




def calculate_bounding_box(center_x, center_y, width, height, scale):
    """计算图案的边界框"""
    half_width = (width * scale) / 2
    half_height = (height * scale) / 2
    deviation = math.hypot(width / 2, height / 2)

    return {
        "left": center_x - deviation,
        "right": center_x + deviation,
        "top": center_y - deviation,
        "bottom": center_y + deviation,
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


def is_overlap_too_high(new_box, existing_boxes, max_overlap_ratio=0.01):
    """检测新边界框是否与已有边界框重叠过多"""
    for box in existing_boxes:
        overlap_area = calculate_overlap_area(new_box, box)
        # 计算重叠比例
        new_box_area = (new_box["right"] - new_box["left"]) * (new_box["bottom"] - new_box["top"])
        if new_box_area > 0 and (overlap_area / new_box_area) > max_overlap_ratio:
            return True  # 重叠比例过高
    return False


def adjust_position_to_fit_bounds(cx, cy, width, height, scale, canvas_size):
    """调整图案位置，确保边界框在画布范围内"""
    half_width = (width * scale) / 2
    half_height = (height * scale) / 2

    # 确保边界框不会超出画布范围
    cx = max(half_width, min(cx, canvas_size - half_width))
    cy = max(half_height, min(cy, canvas_size - half_height))
    return cx, cy


class SignleGA():
    def __init__(self, savename, design_element):
        # 0. parse new design element
        self.design_element = design_element
        doc = minidom.parse(self.design_element)
        self.pathes = [path.getAttribute('d') for path in doc.getElementsByTagName('path')][:-1]
        self.path_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('path')]
        self.bk_color = [path.getAttribute('fill') for path in doc.getElementsByTagName('rect')][0]
        self.width = int([path.getAttribute('width') for path in doc.getElementsByTagName('rect')][0].split(".")[0])
        self.height = int([path.getAttribute('height') for path in doc.getElementsByTagName('rect')][0].split(".")[0])
        
        # 动态调整画板大小：至少为图案的 3 倍尺寸
        self.rect_length = max(3 * self.width, 3 * self.height)
        self.savename = savename
        self.deviation = math.hypot(self.width / 2, self.height / 2)

        # 1. 设置个体与种群
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # 优化问题：最大化适应度
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, 0, self.rect_length)  # 随机生成一个浮点数 [0, rect_length]
        self.toolbox.register("attr_scale", random.uniform, 0.3, 1)  # 随机生成缩放比例 [0.3, 1]
        self.toolbox.register("attr_rotation", random.uniform, 0, 360)  # 随机生成旋转角度 [0, 360]

        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.generate_de_param, n=5)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def generate_de_param(self):
        """生成单个图案的参数"""
        cx = random.uniform(self.deviation, self.rect_length - self.deviation)
        cy = random.uniform(self.deviation, self.rect_length - self.deviation)
        scale = random.uniform(0.3, 1)
        rotation = random.uniform(0, 360)

        # 调整位置以确保边界框在画布范围内
        cx, cy = adjust_position_to_fit_bounds(cx, cy, self.width, self.height, scale, self.rect_length)

        return [cx, cy, scale, rotation]

    def custom_mate(self, ind1, ind2):
        """自定义交叉操作，对每个矩形参数进行交叉"""
        for i in range(len(ind1)):  # 遍历每个矩形
            for j in range(4):  # 遍历 [cx, cy, scale, rotation]
                if random.random() < 0.5:  # 50% 概率交换参数
                    ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]
        return ind1, ind2

    def custom_mutate(self, individual):
        """自定义变异操作，对每个矩形参数进行变异"""
        for rect in individual:  # 遍历每个矩形
            if random.random() < 0.2:  # 20% 概率变异
                rect[0] += random.gauss(0, 10)  # x 坐标变异
                rect[1] += random.gauss(0, 10)  # y 坐标变异
                rect[2] += random.gauss(0, 0.1)  # scale 变异
                rect[3] += random.gauss(0, 5)  # rotation 变异
                # 确保参数在合理范围内
                rect[0] = max(self.deviation, min(rect[0], self.rect_length - self.deviation))
                rect[1] = max(self.deviation, min(rect[1], self.rect_length - self.deviation))
                rect[2] = max(0.3, min(rect[2], 1))
                rect[3] = rect[3] % 360  # rotation 限制在 [0, 360]
        return individual

    def _single_pattern(self, individual):
        """生成单个图案的 SVG 内容"""
        patternes = []
        existing_boxes = []  # 存储已有图案的边界框

        # # 添加背景矩形
        # rect = f'<rect width="{self.rect_length}" height="{self.rect_length}" fill="{self.bk_color}"/>'
        # patternes.append(rect)

        for n, rect in enumerate(individual):
            cx, cy, scale, rotation = rect

            # 调整位置以确保边界框在画布范围内
            cx, cy = adjust_position_to_fit_bounds(cx, cy, self.width, self.height, scale, self.rect_length)

            # 计算当前图案的边界框
            new_box = calculate_bounding_box(cx, cy, self.width, self.height, scale)

            # 检测重叠
            attempts = 0
            while is_overlap_too_high(new_box, existing_boxes, max_overlap_ratio=0.1):
                rect[0] = random.uniform(self.deviation, self.rect_length - self.deviation)
                rect[1] = random.uniform(self.deviation, self.rect_length - self.deviation)
                cx, cy = adjust_position_to_fit_bounds(rect[0], rect[1], self.width, self.height, scale, self.rect_length)
                new_box = calculate_bounding_box(cx, cy, self.width, self.height, scale)
                attempts += 1
                if attempts > 100:
                    print(f"Warning: Unable to place element {n} without excessive overlap.")
                    break

            existing_boxes.append(new_box)
            transform = f'translate({cx:.1f},{cy:.1f}) rotate({rotation:.1f}) scale({scale:.1f})'
            g_tag = f'<g id="de{n}" transform="{transform}">'
            patternes.append(g_tag)
            prop1 = 'transform="translate(0.0,0.0) scale(0.1,-0.1)" stroke="none" fill="'
            for i in range(len(self.pathes)):
                patternes.append(f'<path d="{self.pathes[i]}" {prop1}{self.path_color[i]}"/>')
            patternes.append('</g>')

        return patternes

    def draw_single_pattern(self, individual):
        t = 2
        """绘制单个 SVG 图案"""
        patterns = self._single_pattern(individual)
        header = f'<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="{self.rect_length * t}pt" \
                height="{self.rect_length * t}pt" viewBox="0 0 {self.rect_length * t} {self.rect_length * t}" preserveAspectRatio="xMidYMid meet">'
        bk_rect = '<rect width="' + str(self.rect_length * t) + '" height="' + str(self.rect_length * t) + \
                '" fill="' + str(self.bk_color) + '"/>'
        
        rowgroup = []
        for i in range(t):
            for j in range(t):
                grouppath = (
                    f'<g id="{i}_{j}" transform="translate({j * self.rect_length},{i * self.rect_length}) scale(1,1)">\n'
                )
                rowgroup.append(grouppath)
                for path in patterns:
                    rowgroup.append(path)
                rowgroup.append('</g>' + '\n')

        with open(self.savename, 'w') as svg:
            svg.write('<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            svg.write(header + '\n')
            svg.write('<metadata>\nCreated by ZoeQu, written in 2024\n</metadata>\n')
            svg.write(bk_rect  + '\n')

            for k in rowgroup:
                svg.write(k + '\n')
            svg.write("</svg>")
        svg.close()

        # self.svg_visualization()


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
        

    # def generate_pattern(self):
    #     """生成图案"""
    #     self.toolbox.register("mate", self.custom_mate)
    #     self.toolbox.register("mutate", self.custom_mutate)
    #     self.toolbox.register("select", tools.selTournament, tournsize=3)

    #     population = self.toolbox.population(n=10)
    #     for generation in range(100):
    #         print(f"Generation {generation + 1}")
    #         individual = random.choice(population)
    #         self.draw_single_pattern(individual)
    #         feedback = input("Do you like this layout? (y/n): ").strip().lower()
    #         if feedback == 'y':
    #             print("Optimization finished! Final layout:")
    #             self.draw_single_pattern(individual)
    #             break
    #         offspring = self.toolbox.select(population, len(population))
    #         offspring = list(map(self.toolbox.clone, offspring))
    #         for child1, child2 in zip(offspring[::2], offspring[1::2]):
    #             if random.random() < 0.5:
    #                 self.toolbox.mate(child1, child2)
    #                 del child1.fitness.values
    #                 del child2.fitness.values
    #         for mutant in offspring:
    #             if random.random() < 0.2:
    #                 self.toolbox.mutate(mutant)
    #                 del mutant.fitness.values
    #         population[:] = offspring
    #     print("Process finished.")
        
    def generate_pattern(self):
        """生成图案"""
        self.toolbox.register("mate", self.custom_mate)
        self.toolbox.register("mutate", self.custom_mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        self.population = self.toolbox.population(n=10)  # 初始化种群
        self.current_generation = 0  # 当前代数

        self.candidates = []  # 清空候选个体

        svg_names = []  # 保存生成的图案路径
        for i in range(6):  # 生成 6 个图案
            individual = random.choice(self.population)  # 从种群中随机选择一个个体
            svg_name = f"{self.savename.replace('.svg', '')}_gen_{i}.svg"
            self.savename = svg_name
            self.draw_single_pattern(individual)  # 绘制图案并保存
            print(f"Generated {svg_name}")
            svg_names.append(svg_name)
            self.candidates.append(individual)  # 保存当前代候选个体

        return svg_names  # 返回第一代图案路径

        
    def generate_next_iteration(self, selected_indices):
        """生成下一代图案"""
        if self.current_generation >= 100:  # 达到最大代数时停止
            print("Reached maximum generations.")
            return

        print(f"Generation {self.current_generation + 1}")

        # Step 1: 从用户选择的索引中提取对应的个体
        selected_individuals = [self.candidates[idx] for idx in selected_indices]

        if not selected_individuals:
            print("No designs selected. Exiting...")
            return []

        # Step 2: 基于用户选择的图案生成下一代
        offspring = []
        while len(offspring) < len(self.population):  # 保持种群大小不变
            # 随机选择两个父代进行交叉
            parent1, parent2 = random.sample(selected_individuals, 2)
            child1, child2 = self.toolbox.clone(parent1), self.toolbox.clone(parent2)

            # 交叉操作
            if random.random() < 0.5:  # 50% 概率进行交叉
                self.toolbox.mate(child1, child2)

            # 变异操作
            if random.random() < 0.2:  # 20% 概率进行变异
                self.toolbox.mutate(child1)
            if random.random() < 0.2:
                self.toolbox.mutate(child2)

            offspring.append(child1)
            if len(offspring) < len(self.population):  # 如果未达到种群大小，添加第二个子代
                offspring.append(child2)

        # 更新种群为新一代
        self.population[:] = offspring
        self.current_generation += 1  # 更新代数

        # Step 3: 生成新一代图案
        svg_names = []  # 保存生成的图案路径
        self.candidates = []  # 更新当前代的候选个体
        for i in range(6):  # 生成 6 个图案
            individual = random.choice(self.population)  # 从种群中随机选择一个个体
            svg_name = f"{self.savename.replace('.svg', '')}_gen_ind_{i}.svg"
            self.savename = svg_name
            self.draw_single_pattern(individual)  # 绘制图案并保存
            print(f"Generated {svg_name}")
            svg_names.append(svg_name)
            self.candidates.append(individual)

        print(f"Finished generation {self.current_generation}.")
        return svg_names  # 返回新一代图案路径

    # def generate_next_iteration(self):
    #     """生成下一代图案"""
    #     if self.current_generation >= 100:  # 达到最大代数时停止
    #         print("Reached maximum generations.")
    #         return

    #     print(f"Generation {self.current_generation + 1}")
    #     individual = random.choice(self.population)
    #     self.draw_single_pattern(individual)  # 绘制当前图案
    #     self.current_individual = individual  # 保存当前个体

    #     # 更新代数
    #     self.current_generation += 1
    #     print("Process finished.")

if __name__ == "__main__":
    design_element = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/svg/test_filter_num_28.svg"
    svgname = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/temp_save/test.svg"
    single_ga = SignleGA(svgname, design_element)
    single_ga.generate_pattern()