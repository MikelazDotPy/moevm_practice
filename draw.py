from io import BytesIO
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from target_func import SquarePlaceData, debug_M

def draw_squares_in_circle(r, h, squares: SquarePlaceData):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    for square in squares:
        for i in range(square.length):
            ax.add_patch(
                patches.Rectangle(
                (square.x, square.y + h*i), h, h,
                linewidth=1, edgecolor='red', facecolor='none'
            )
            )

    ax.add_patch(plt.Circle((0, 0), r, fill=False, color='blue', linewidth=2))

    ax.set_xlim(-r - 1, r + 1)
    ax.set_ylim(-r - 1, r + 1)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.title(f'Сторона квадрата h = {h}')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig) 
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    r = 20
    h = 9.32
    k = 8
    data = debug_M(r, h, k)
    with open("output.png", "wb") as f:
        f.write(draw_squares_in_circle(r, h, data.squares))
