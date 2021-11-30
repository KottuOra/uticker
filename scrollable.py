import logging
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import unicodedata

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

class Scrollable:
    image=None
    font=None
    category=None
    color=None
    display_width = 0
    display_height = 0
    lengths=[]

    def __init__(self, category, content, color,font, canvasshape):
        self.category = category
        self.content = content
        self.color = color
        self.font = font
        self.display_width, self.display_height = canvasshape
        self.render_image()

    def getTickerLines(self):
        resultset=[]
        try:
            for key,value in self.content.items():
                resultset.append(key)
                #for line in values:
                    #normalized = unicodedata.normalize('NFD', line)
                    #new_str = u"".join([c for c in normalized if not unicodedata.combining(c)])
                resultset.append(value)
        except:
            resultset.append["Error rendering content!"]
        return resultset

    def render_image(self):
        lines = self.getTickerLines()
        self.lengths = [0] * len(lines)
        for line, text in enumerate(lines):
            text_width, text_height = self.font.getsize(text)
            paddedwidth = text_width + self.display_width
            self.lengths [line] = paddedwidth
        maxwidth = max (self.lengths)
        logging.debug("prepared the image with max width: %s", maxwidth)

        # Create a new PIL image big enough to fit the text
        self.image = Image.new('P', (maxwidth, self.display_height * len(lines)*2), 0)
        draw = ImageDraw.Draw(self.image)
        y_offset = 0
        for line, text in enumerate(lines):
            # Draw the text into the image
            y_offset += self.display_height
            draw.text((0, y_offset-2), text, font=self.font, fill=255)
            y_offset += self.display_height
        #image.save("out/"+self.category + ".png")


def main():
    logging.debug("Starting the scrollable main")
    content = {"{sample key}":"sample content","{second key}":"abcdefghijklmnopqrstuvwxyz."}
    font = ImageFont.truetype("fonts/dotm.ttf", 8) 
    shape = (17,7)
    scrollable = Scrollable("sample 1",content,(255,255,255),font,shape)

    content = {"{ key1}":"content 1","{ key2}":"content 2","{ key3}":"content 3"}
    scrollable = Scrollable("sample 2",content,(255,255,255),font,shape)

if __name__ == "__main__":
    main()