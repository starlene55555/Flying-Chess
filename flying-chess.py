import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# **第一行 Streamlit 指令**
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 使用 CSS 清除頁面頂部空白
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0rem;
        margin-top: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 定義多條線段，每條線段給一個公式和格子數


def line1(t):
    return 5.5, 3.85 - 8.85 * t  # 右邊直線


def line2(t):
    return 5.5 - 11 * t, -5  # 最底線


def line3(t):
    return -5.5, -5 + 8.85 * t  # 左邊直線


def line4(t):
    return -5.5 + 5.5 * t, 3.85 + 5.5 * t  # 左斜線


def line5(t):
    return 5.5 * t, 9.35 - 5.5 * t  # 右斜線


def line6(t):
    return 3.5 - 3.5 * t, 5.85 - 3.675 * t  # 冠佑終點線


def line7(t):
    return -5.5 * t + 5.5, -1.775 + 3.95 * t  # 老大終點線


def line8(t):
    return 0, -3 + 5.175 * t  # 瑪莎終點線


def line9(t):
    return -5.5 + 5.5 * t, 6.95 / 11 + 3395 / 2200 * t  # 石拔終點線


def line10(t):
    return -3.5 + 3.5 * t, 5.85 - 3.675 * t  # 阿宏終點線


def line11(t):
    return -5.5, 3.85 + 4.15 * t  # 皇冠線左直


def line12(t):
    return -5.5 + 2 * t, 8 - 2.15 * t  # 皇冠線左斜


def line13(t):
    return 3.5 + 2 * t, 5.85 + 2.15 * t  # 皇冠線右斜


def line14(t):
    return 5.5, 8 - 4.15 * t  # 皇冠線右直


def line15(t):
    return -1.5 * t, -3 - 2 * t  # 皇冠線左下


def line16(t):
    return 1.5 - 1.5 * t, -5 + 2 * t  # 皇冠線右下


# ===== 外圍框框格子 =====
def generate_normal_grids(formula_nor, num_cells, skip_first=False):
    grids_nor = []
    normal_t_values = np.linspace(0, 1, num_cells + 1)
    if skip_first:
        normal_t_values = normal_t_values[1:]  # 跳過第一個點避免重疊
    for t in normal_t_values:
        x, y = formula_nor(t)
        grid_nor = {
            "x": x,
            "y": y,
            "type": "normal",
            "color": None,
            "stackable": True,
            "occupied_by": [],
            "id": None
        }
        grids_nor.append(grid_nor)
    return grids_nor


# 生成所有普通格子
all_grids = []

all_grids += generate_normal_grids(line1, 11)  # 第一條線
all_grids += generate_normal_grids(line2, 11, skip_first=True)
all_grids += generate_normal_grids(line3, 11, skip_first=True)
all_grids += generate_normal_grids(line4, 11, skip_first=True)
all_grids += generate_normal_grids(line5, 11, skip_first=True)

# ===== 顏色分配函數 =====
colors = ["#69CAFF", "#E87361", "#F6E039", "#A0FF89", "#FF96CC"]
# 冠佑藍、老大紅、瑪莎黃、石拔綠、阿宏粉


def assign_colors(grids_nor_colours, palette, start_index=0):
    n_colors = len(palette)
    for idx_nor, grid_nor_colours in enumerate(grids_nor_colours):
        color_idx = (idx_nor + start_index) % n_colors
        grid_nor_colours["color"] = palette[color_idx]


# ===== 排顏色 =====
all_grids = []
line1_grids = generate_normal_grids(line1, 11, skip_first=True)
assign_colors(line1_grids, colors, start_index=0)

line2_grids = generate_normal_grids(line2, 11, skip_first=True)
assign_colors(line2_grids, colors, start_index=1)

line3_grids = generate_normal_grids(line3, 11, skip_first=True)
assign_colors(line3_grids, colors, start_index=2)

line4_grids = generate_normal_grids(line4, 11, skip_first=True)
assign_colors(line4_grids, colors, start_index=3)

line5_grids = generate_normal_grids(line5, 11, skip_first=True)
assign_colors(line5_grids, colors, start_index=4)

# 合併
all_grids += line1_grids + line2_grids + line3_grids + line4_grids + line5_grids

# 生成id
for idx, grid in enumerate(all_grids, start=1):
    grid["id"] = f"normal_{idx}"

# 終點線
goal_lines = [
    (line6, colors[0], 6),  # 藍，6格
    (line7, colors[1], 6),  # 紅，6格
    (line8, colors[2], 6),  # 黃，6格
    (line9, colors[3], 6),  # 綠，6格
    (line10, colors[4], 9),  # 粉紅，9格（特例）
]


# 做格子
def generate_goal_grids(line_formula, owner_color, grid_count):

    # line_formula: 終點線座標函數
    # owner_color: 該終點線顏色字串（例如 "#69CAFF"）
    # grid_count: 終點線格子數，不含最後中心終點

    grids_goal = []

    # t_values 從 0 開始，但跳過 0（避免重疊普通線的格子）
    t_values_nor = np.linspace(0, 1, grid_count + 1)[1:]

    for idx_goal, t in enumerate(t_values_nor[:-1]):  # 前 grid_count-1 個格子
        x, y = line_formula(t)
        grids_goal.append({
            "x": x,
            "y": y,
            "type": "goal",
            "color": owner_color,
            "stackable": True,
            "occupied_by": None,
            "id": f"{owner_color}_{idx_goal + 1}"
        })

    # 最後一格作為中心終點
    x_end, y_end = line_formula(1)
    grids_goal.append({
        "x": x_end,
        "y": y_end,
        "type": "goal",
        "color": owner_color,
        "stackable": False,
        "occupied_by": None,
        "id": f"{owner_color}_end"
    })

    return grids_goal


all_goal_grids = []

for line_func, color, n in goal_lines:
    goal_segment = generate_goal_grids(line_func, color, n)
    all_goal_grids += goal_segment

# 皇冠線
# 例子：每個元素代表一條繞道，內部是兩條線段及其格子數
# detours = [
#    [(line11, 4), (line12, 4)],  # 左上
#    [(line13, 4), (line14, 4)],  # 右上
#    [(line16, 3), (line15, 4)],   # 下面
# ]

# ===== 皇冠線 =====

# 每段繞道： (線段公式, 格子數, 顏色清單)
detour_segments = [
    (line11, 5, [colors[3], colors[4], colors[0], colors[1], colors[2]], "line11"),  # 繞道 1-1
    (line12, 4, [colors[3], colors[4], colors[0], colors[1]], "line12"),  # 繞道 1-2
    (line13, 4, [colors[1], colors[2], colors[3], colors[4]], "line13"),  # 繞道 2-1
    (line14, 4, [colors[1], colors[2], colors[3], colors[4]], "line14"),  # 繞道 2-2
    (line16, 3, [colors[0], colors[1], colors[2]], "line16"),  # 繞道 3-1
    (line15, 5, [colors[3], colors[4], colors[0], colors[1], colors[2]], "line15"),  # 繞道 3-2
]


# ===== 生成繞道格 =====
def generate_detour_grids(detour_seg):
    detour_g = []
    for idxxx, (formula, count, manual_colors, line_name) in enumerate(detour_seg, start=1):
        grids = generate_normal_grids(formula, count, skip_first=True)

        # 如果是 line12, line14, line15，就去掉最後一格
        if line_name in ["line12", "line14", "line15"]:
            grids = grids[:-1]

        # 填入手動顏色並設定疊加屬性
        for j, (go, co) in enumerate(zip(grids, manual_colors), start=1):
            go["color"] = co
            go["type"] = "detour"
            go["id"] = f"detour{idxxx}_{j}"
            go["stackable"] = True          # 允許疊加
            go["collective_move"] = True    # 同一格棋子一起移動
            go["occupied_by"] = []          # 初始化為空 list
        detour_g += grids
    return detour_g


detour_grids = generate_detour_grids(detour_segments)


# 飛行格
def generate_flight_grid(colors_flight):
    flight_grids = {
        "x": 0,
        "y": 10,
        "type": "flight",         # 飛行格類型
        "color": "grey",            # 無顏色
        "stackable": True,        # 可以疊加同色棋子
        "occupied_by": [],        # 用 list 來存放棋子
        "id": "flight",           # 唯一編號
        "flight_targets": {       # 飛行目的地對應玩家顏色
            colors_flight[0]: [13, 20],     # 可飛到的普通格編號
            colors_flight[1]: [13, 20],
            colors_flight[3]: [13, 20],
            colors_flight[2]: [13],       # 黃色玩家限制只能飛到 13
            colors_flight[4]: [13, 20]
        }
    }
    return flight_grids


flight_grid = generate_flight_grid(colors)

# 定義五個起跑道格子
start_runway_grids = [
    {"x": 6.5, "y": 4.5, "color": colors[0]},     # 玩家1
    {"x": 6.5, "y": -5.5, "color": colors[1]},    # 玩家2
    {"x": -6, "y": -6, "color": colors[2]},    # 玩家3
    {"x": -6.5, "y": 3, "color": colors[3]},   # 玩家4
    {"x": -0.8, "y": 9.8, "color": colors[4]},   # 玩家5
]


all_grids += all_goal_grids + detour_grids + [flight_grid] + start_runway_grids


# 飛行線
def flight_route_a(t):  # 右邊
    x = (1-t)**3*0 + 3*(1-t)**2*t*1.75 + 3*(1-t)*t**2*2.75 + t**3*3.5
    y = (1-t)**3*9.35 + 3*(1-t)**2*t*4.0125 + 3*(1-t)*t**2*0.2 + t**3*-5
    return x, y


def flight_route_b(t):  # 左邊

    x = (1 - t) ** 3 * 0 + 3 * (1 - t) ** 2 * t * (-1.94444) + 3 * (1 - t) * t ** 2 * (-2.75) + t ** 3 * -3.5
    y = (1 - t) ** 3 * 9.35 + 3 * (1 - t) ** 2 * t * 4.2167 + 3 * (1 - t) * t ** 2 * 1.40341 + t ** 3 * -5
    return x, y


flight_path_intersections = {
    flight_route_a: ["#69CAFF_3", "#E87361_3"],  # 航線 A 會飛過的終點格
    flight_route_b: ["#FF96CC_4", "#FF96CC_5", "#A0FF89_3"]   # 航線 B 會飛過的終點格
}


# 在頁面最上方占位
plot_placeholder = st.empty()  # 這裡不會渲染任何內容，但保留一個位置


# Streamlit 入口，程式每次啟動或重新整理時執行
if "all_grids" not in st.session_state:
    st.session_state.all_grids = []  # 或者清空舊資料

    # 生成普通格
    st.session_state.all_grids += line1_grids
    st.session_state.all_grids += line2_grids
    st.session_state.all_grids += line3_grids
    st.session_state.all_grids += line4_grids
    st.session_state.all_grids += line5_grids

    # 生成終點格
    st.session_state.all_grids += all_goal_grids

    # 生成繞道格
    st.session_state.all_grids += generate_detour_grids(detour_segments)

    # 生成飛行格
    st.session_state.all_grids.append(generate_flight_grid(colors))

    # 生成起點格
    st.session_state.all_grids += start_runway_grids


# 在streamlit上呈現
plot_placeholder = st.empty()
airport_placeholder = st.empty()

scale = 0.15
fig, ax = plt.subplots(figsize=(12*scale, 8*scale))
fig.subplots_adjust(top=0.95, bottom=0.05)  # top 越大，圖越往上
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 11.5)
ax.set_aspect("equal", adjustable="box")
ax.axis('off')  # 隱藏座標軸

for g in st.session_state.all_grids:
    rect = plt.Rectangle((g["x"]-0.25, g["y"]-0.25), 0.5, 0.5,
                         facecolor=g["color"], edgecolor="black", linewidth=0.25)
    ax.add_patch(rect)

# 把圖表渲染到最上方占位
plot_placeholder.pyplot(fig, dpi=500, use_container_width=False)


# 假設五個顏色，每個顏色 3 顆棋子
colors = [colors[0], colors[1], colors[2], colors[3], colors[4]]
for color in colors:
    cols = st.columns(3)  # 每排3個棋子
    for i, col in enumerate(cols):
        col.button("●", key=f"{color}_{i}", disabled=True,
                   style=f"font-size:24px;color:{color};border:none;background:none")

# /Users/crystaltang/Documents/_Beloved/MAYDAY/MAYDAY-GAME/FLYING-CHESS
# python3 Flying-Chess.py
# streamlit run Flying-Chess.py
