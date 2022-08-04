# -*- coding: utf-8 -*-
import os
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor 
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn


cwd = os.getcwd()
path_to_docx = os.path.join(cwd, "document.docx")

path_to_src = "D:\\GitHub\machine-learning-cheat-sheet\machine-learning-cheat-sheet.tex"
name_f = os.path.basename(path_to_src)
f = open(path_to_src,'r', encoding="utf-8")
text_str = f.read()
f.close()

# создание документа
doc = Document()
# задаем стиль текста по умолчанию
style = doc.styles['Heading 1']
# название шрифта
style.font.name = 'Times New Roman'
# размер шрифта
style.font.size = Pt(14)

rFonts = style.element.rPr.rFonts
rFonts.set(qn("w:asciiTheme"), "Times New Roman")
rFonts.set(qn("w:hAnsiTheme"), "Times New Roman")
print(style.element.xml)

style.font.color.rgb = RGBColor(0, 0, 0)
head = doc.add_heading('1.\t'+name_f, 1)
h_fmt = head.paragraph_format
h_fmt.line_spacing = 1.5 #Межстрочный интервал 
h_fmt.space_before = Pt(0)
h_fmt.space_after = Pt(0)  #интервал после абзаца.
h_fmt.first_line_indent = Cm(1.5) #Отступ первой (красной) строки 

section = doc.sections[0]
# левое поле в сантиметрах
section.left_margin = Cm(2)
# правое поле в сантиметрах
section.right_margin = Cm(1)
# верхнее поле в сантиметрах
section.top_margin = Cm(2)
# нижнее поле в сантиметрах
section.bottom_margin = Cm(2) 

style = doc.styles['Normal']
style.font.size = Pt(14)
style.font.name = 'Times New Roman'

p = doc.add_paragraph(text_str)
# добавляем текст прогоном 
run = p.add_run()
# run = p.add_run('символов текста.')
run.add_break(WD_BREAK.PAGE)

p_fmt = p.paragraph_format
p_fmt.line_spacing = 1.5 #Межстрочный интервал 
p_fmt.space_before = Pt(0)
p_fmt.space_after = Pt(0)  #интервал после абзаца.
p_fmt.first_line_indent = Cm(1.5) #Отступ первой (красной) строки 


doc.save(path_to_docx)


