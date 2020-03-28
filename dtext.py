#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import logging
from PIL import Image,ImageDraw,ImageFont
import textwrap
import traceback
import pygame
from pygame import freetype

_cjkranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def _is_cjk(char):
    """"_is_cjk(char: string) -> bool
     Checks whether character is CJK.

        >>> is_cjk(u'\u33fe')
        True
        >>> is_cjk(u'\uFE5F')
        False

    """
    return any([range["from"] <= ord(char) <= range["to"] for range in _cjkranges])

class textbox:
    """
    Object for draw text on the pic
    """
    def __init__(self,
                 box_size, 
                 font,
                 color,
                 bgcolor,
                 alignment="L",
                 row_spaces=3,
                 Limage=True):
        self.box_size_x = box_size[0] 
        self.box_size_y = box_size[1] 
        self.font = font
        self.alignment = alignment
        self.text_out_of_box = ""
        self.row_spaces = row_spaces
        self.color = color
        self.bgcolor = bgcolor
        self.y_offset = 0
        self.box = (0,0) 
        self.Limage = Limage

    def _split_text(self, text):
        """_split(text)(text: string) -> [string]

        Split the text to each line
        """
        maxlinewidth = int((self.box_size_x)//(self.font.size//2))
        spchunks = text.splitlines()
        self.text_out_of_box = ""
        lines = []
        for chunks in spchunks:
            if len(chunks) == 0:
                lines.append(chunks)
            while len(chunks) >0:
                linewidth = maxlinewidth
                while True:
                    wtext = chunks[:self.box_size_x] 
                    if _is_cjk(wtext[:linewidth][-1]):
                        line = [(wtext[:linewidth])]
                    else:
                        line = textwrap.wrap(wtext, width=linewidth,replace_whitespace=False,drop_whitespace=False)
                    rlinewidth = self.font.get_rect(line[0]).width
                    dlinewidth = rlinewidth - self.box_size_x
                    offset = (dlinewidth//self.font.size)//2
                    if rlinewidth <= self.box_size_x:
                        lines.append(line[0])
                        chunks = chunks[len(line[0]):]
                        linewidth = maxlinewidth
                        if len(chunks) == 0:
                            break
                    elif offset == 0:
                        linewidth = linewidth - 1
                    else:
                        linewidth = int(linewidth - offset)
        return lines

    def draw_text(self,text,offset=False):
        """draw_text(text,offset)(text: string,offset: bool) -> PIL.Image.Image

        return a image with given text
        """
        if not offset :
            self.y_offset = 0
        lines = self._split_text(text)
        strFormat = 'RGBA'
        image = Image.new('RGBA', (self.box_size_x,self.box_size_y), self.bgcolor)
        draw = ImageDraw.Draw(image)
        for line in lines:
            height = int(self.font.size)
            if self.y_offset + height > self.box_size_y:
                self.text_out_of_box += line
            else:
                rtext = self.font.render(line,self.color,self.bgcolor)
                raw_str = pygame.image.tostring(rtext[0], strFormat, False)
                textimage = Image.frombytes(strFormat, rtext[0].get_size(), raw_str)
                width = textimage.size[0]
                if self.alignment == "R":
                    image.paste(textimage,(self.box_size_x - width,self.y_offset),textimage)
                elif self.alignment == "C":
                   image.paste(textimage,(int((self.box_size_x - width)/2),self.y_offset),textimage)
                elif self.alignment == "L":
                   image.paste(textimage,(0,self.y_offset),textimage)
                else:
                    raise Exception("Invalid alignment!", self.alignment)
                self.y_offset += (height+self.row_spaces)
        if self.Limage :
            image8bit = image.convert("L")
            return image8bit
        else:
            return image
    
    def draw_remain_text(self):
        if len(self.text_out_of_box) != 0:
            return self.draw_text(self.text_out_of_box)
        else:
            image = Image.new('RGBA', (0,0), self.bgcolor)
            return image

    def draw_box(self,text,box,image,offset=False):
        textimage=self.draw_text(text,offset)
        self.box = box
        image.paste(textimage,self.box,textimage)

    def draw_next_box(self,image):
        textimage=self.draw_remain_text()
        image.paste(textimage,self.box,textimage)



