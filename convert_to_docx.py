# -*- coding: utf-8 -*-
import os
import docx
import glob
from docx import Document
from docx.shared import Pt, Cm, RGBColor 
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn

class Src2Docx():
    
    def __init__(self, template):
        self.doc = Document(template)
        section = self.doc.sections[0]
        section.left_margin = Cm(2)
        section.right_margin = Cm(1)
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2) 
        
    def add_heading(self, file_bn):
        style = self.doc.styles['Heading 1']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(14)
        rFonts = style.element.rPr.rFonts
        rFonts.set(qn("w:asciiTheme"), "Times New Roman")
        rFonts.set(qn("w:hAnsiTheme"), "Times New Roman")
        style.font.color.rgb = RGBColor(0, 0, 0)
        head = self.doc.add_heading(file_bn, 1)
        h_fmt = head.paragraph_format
        h_fmt.line_spacing = 1.5
        h_fmt.space_before = Pt(0)
        h_fmt.space_after = Pt(0)
        h_fmt.first_line_indent = Cm(1.5)
        
    def add_paragraph(self, text):
        style = self.doc.styles['Normal']
        style.font.size = Pt(14)
        style.font.name = 'Times New Roman'
        p = self.doc.add_paragraph(text)
        run = p.add_run()
        run.add_break(WD_BREAK.PAGE)
        p_fmt = p.paragraph_format
        p_fmt.line_spacing = 1.5
        p_fmt.space_before = Pt(0)
        p_fmt.space_after = Pt(0)
        p_fmt.first_line_indent = Cm(1.5)
        
    def add_koll(self, texth):
        header = self.doc.sections[0].header.paragraphs[0]
        header.style.font.size = Pt(14)
        header.style.font.name = 'Times New Roman'
        header.add_run(texth)
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    def save_docx(self, path):
        self.doc.save(path)
        
def get_files(folder):
    extensions = ['cpp', 'h']
    path_to_conf = ".filesextension"

    f = open(path_to_conf,'r', encoding="utf-8")
    extensions = f.read()
    f.close()
    extensions = extensions.split("\n")
    res = []    
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if path.split('.')[-1] in extensions:
                res.append(path)
    return res


path_to = "D:\\GitHub\machine-learning-cheat-sheet"

cwd = os.getcwd()
path_to_docx = os.path.join(cwd, "document.docx")

files = get_files(path_to)

docc = Src2Docx('D:\\GitHub\\Prorgams-text-to-docx\\template.docx')
for i in files:
    print(i)
    name_f = os.path.basename(i)
    f = open(i,'r', encoding="utf-8")#, errors='ignore')
    text_str = f.read()
    f.close()
    
    docc.add_heading(name_f)
    docc.add_paragraph(text_str)
    
#docc.add_koll(koll)
docc.save_docx(path_to_docx)


