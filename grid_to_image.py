from PIL import Image, ImageDraw, ImageFont

# cole a função abaixo no seu projeto
def render_sudoku(
    grid,
    cell_size=64,
    margin=24,
    line_thin=2,
    line_thick=6,
    bg_color="white",
    line_color="black",
    text_color="black",
    outfile="sudoku.png",
):
    # validação simples
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Grid must be 9x9.")
    grid_px = 9 * cell_size
    W = H = grid_px + 2 * margin

    img = Image.new("RGB", (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)

    # tenta usar uma fonte boa; se não achar, usa a default
    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        try:
            font = ImageFont.truetype(fp, size=int(cell_size * 0.55))
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()

    def line(x0, y0, x1, y1, thick=False):
        draw.line((x0, y0, x1, y1), fill=line_color, width=(line_thick if thick else line_thin))

    # bordas e linhas
    left = top = margin
    right = bottom = margin + grid_px
    for i in range(10):
        x = left + i * cell_size
        y = top + i * cell_size
        line(x, top, x, bottom, thick=(i % 3 == 0))
        line(left, y, right, y, thick=(i % 3 == 0))

    # escreve números (0/None são vazios)
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val in (0, None, ""):
                continue
            cx = left + c * cell_size + cell_size / 2
            cy = top + r * cell_size + cell_size / 2
            text = str(val)
            try:
                draw.text((cx, cy), text, fill=text_color, font=font, anchor="mm")
            except TypeError:
                # fallback caso PIL não suporte anchor="mm"
                w, h = draw.textbbox((0, 0), text, font=font)[2:]
                draw.text((cx - w/2, cy - h/2), text, fill=text_color, font=font)

    img.save(outfile, "PNG")
    return outfile


