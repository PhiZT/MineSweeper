from tkinter import Button, Label
import random
import settings
import ctypes
import os
import sys


class Cell:
    all = []
    cell_counter = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self,x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_open = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions ) # 左键操作
        btn.bind('<Button-2>', self.right_click_actions ) # 右键操作
        self.cell_btn_object = btn

    @staticmethod
    def creat_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"剩余格子数: {Cell.cell_counter}",
            width=12,
            height=4,
            font=("Arial", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

            # 提示游戏通关
            if Cell.cell_counter == settings.MINES_COUNT:
                os.system(
                    "osascript -e 'Tell application \"System Events\" to display dialog \""f" 扫雷成功""\" with title \""f"恭喜""\"'"
                )
                sys.exit(0)

        # 确保已经被点开的格子就不能再被标记了,很小的bug但是很恶心
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-2>')

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(text="🚩")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                text=""
            )
            self.is_mine_candidate = False

    def get_cell_by_axis(self, x,y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y -1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_open:
            Cell.cell_counter -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"剩余格子数: {Cell.cell_counter}"
                )
        # 标注格子为已打开去除bug
        self.is_open = True

    def show_mine(self):
        self.cell_btn_object.configure(text="💣")
        # 提醒游戏失败
        os.system(
            "osascript -e 'Tell application \"System Events\" to display dialog \""f" 嘭！游戏结束""\" with title \""f"踩雷了""\"'"
        )
        sys.exit(0)

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"