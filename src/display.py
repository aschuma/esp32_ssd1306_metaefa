import gfx
import ssd1306


class Display(ssd1306.SSD1306_I2C):

    def __init__(self, i2c):
        ssd1306.SSD1306_I2C.__init__(self, 128, 64, i2c)
        self.gfx = gfx.GFX(128, 64, self.pixel, hline=self.hline, vline=self.vline)

    def rect(self, x0, y0, width, height, *args, **kwargs):
        self.gfx.rect(x0, y0, width, height, *args, **kwargs)

    def fill_rect(self, x0, y0, width, height, *args, **kwargs):
        self.gfx.fill_rect(x0, y0, width, height, *args, **kwargs)

    def line(self, x0, y0, x1, y1, *args, **kwargs):
        self.gfx.line(x0, y0, x1, y1, *args, **kwargs)

    def circle(self, x0, y0, radius, *args, **kwargs):
        self.gfx.circle(x0, y0, radius, *args, **kwargs)

    def fill_circle(self, x0, y0, radius, *args, **kwargs):
        self.gfx.fill_circle(x0, y0, radius, *args, **kwargs)

    def triangle(self, x0, y0, x1, y1, x2, y2, *args, **kwargs):
        self.gfx.triangle(x0, y0, x1, y1, x2, y2, *args, **kwargs)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, *args, **kwargs):
        self.gfx.fill_triangle(x0, y0, x1, y1, x2, y2, *args, **kwargs)

    def center_rect(self, scale, *args, **kwargs):
        s = float(scale)
        w = s * self.width
        h = s * self.height
        self.rect(int((self.width - w) / 2.0), int((self.height - h) / 2.0), int(w), int(h), *args, **kwargs)

    def center_fill_rect(self, scale, *args, **kwargs):
        s = float(scale)
        w = s * self.width
        h = s * self.height
        self.fill_rect(int((self.width - w) / 2.0), int((self.height - h) / 2.0), int(w), int(h), *args, **kwargs)

    def center_circle(self, scale, *args, **kwargs):
        s = float(scale)
        r = s * self.width / 2.0
        self.circle(int(self.width / 2.0), int(self.height / 2.0), int(r), *args, **kwargs)

    def center_fill_circle(self, scale, *args, **kwargs):
        s = float(scale)
        r = s * self.width / 2.0
        self.fill_circle(int(self.width / 2.0), int(self.height / 2.0), int(r), *args, **kwargs)
