from PIL import Image, ImageDraw

im = Image.new('RGB', (500, 300), (128, 128, 128))
draw = ImageDraw.Draw(im)
draw.polygon((100, 100, 100, 200, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
# polygon(x1, y1, x2, y2, ...)
im.save("test.jpeg")
