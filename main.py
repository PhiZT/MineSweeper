from tkinter import *
from cell import Cell
import settings
import utils

root = Tk()
# 窗口设置
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("扫雷游戏")
root.resizable(False, False)

# 设置top_frame
top_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_percentage(25)
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text="欢迎来到Tie's扫雷游戏",
    font=("", 48)
)

game_title.place(
    x=utils.width_percentage(35), y=utils.height_percentage(5)
)

# 设置left_frame
left_frame = Frame(
    root,
    bg='black',
    width=utils.width_percentage(25),
    height=utils.height_percentage(75)
)
left_frame.place(x=0, y=utils.height_percentage(25))

# 设置center_frame
center_frame = Frame(
    root,
    bg='black',
    width=utils.width_percentage(75),
    height=utils.height_percentage(75)
)
center_frame.place(
    x=utils.width_percentage(25),
    y=utils.height_percentage(25),
)

# 实例化对象(36个格子)
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y
        )

Cell.randomize_mines()  # 随机生成地雷

# 显示剩余格子数量
Cell.creat_cell_count_label(left_frame)
Cell.cell_count_label_object.place(
    x=0, y=0
)

# Run the window
root.mainloop()
