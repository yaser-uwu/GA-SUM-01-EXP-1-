from pathlib import Path
from io import BytesIO
import json, hashlib, html, textwrap
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
import pdfplumber, pypdfium2
from reportlab.pdfgen import canvas

root = Path.cwd()
font_path = Path('C:/Windows/Fonts/segoeui.ttf')
bold_path = Path('C:/Windows/Fonts/segoeuib.ttf')
font = lambda size, bold=False: ImageFont.truetype(str(bold_path if bold else font_path), size)
W,H=1400,940
im=Image.new('RGB',(W,H),'#F6F5F0'); d=ImageDraw.Draw(im)
mxfile=ET.Element('mxfile',host='app.diagrams.net')
diagram=ET.SubElement(mxfile,'diagram',name='SGRA REST - Khriz',id='sgra-khriz')
model=ET.SubElement(diagram,'mxGraphModel',dx='1400',dy='940',grid='1',gridSize='10',page='1',pageWidth=str(W),pageHeight=str(H))
cells=ET.SubElement(model,'root');ET.SubElement(cells,'mxCell',id='0');ET.SubElement(cells,'mxCell',id='1',parent='0')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#087E81"/></marker></defs>',
 '<rect width="100%" height="100%" fill="#F6F5F0"/>']

def label(key,text,x,y,w,h,size=22,bold=False,box=False,color='#132F3A',fill='#FFFFFF'):
    style=f'whiteSpace=wrap;html=0;fontFamily=Segoe UI;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};'
    style+=f'rounded=1;fillColor={fill};strokeColor=#CDD8D6;' if box else 'text;strokeColor=none;fillColor=none;'
    cell=ET.SubElement(cells,'mxCell',id=key,value=text,vertex='1',parent='1',style=style)
    ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    if box:
        d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill=fill,outline='#CDD8D6',width=2)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#CDD8D6"/>')
    lines=text.split('\n');spacing=size+9;start=y+(h-len(lines)*spacing)/2
    for i,line in enumerate(lines):
        width=d.textlength(line,font=font(size,bold));tx=x+(w-width)/2;ty=start+i*spacing
        d.text((tx,ty),line,font=font(size,bold),fill=color)
        svg.append(f'<text x="{x+w/2}" y="{ty+size}" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(line)}</text>')

def arrow(key,source,target,x1,y1,x2,y2,dashed=False):
    source_geometry=next(c.find('mxGeometry') for c in cells if c.get('id')==source)
    target_geometry=next(c.find('mxGeometry') for c in cells if c.get('id')==target)
    source_y=(y1-float(source_geometry.get('y')))/float(source_geometry.get('height'))
    target_y=(y2-float(target_geometry.get('y')))/float(target_geometry.get('height'))
    anchors=f'exitX={1 if x2>x1 else 0};exitY={source_y};entryX={0 if x2>x1 else 1};entryY={target_y};exitDx=0;exitDy=0;entryDx=0;entryDy=0;'
    cell=ET.SubElement(cells,'mxCell',id=key,edge='1',parent='1',source=source,target=target,
        style='edgeStyle=none;endArrow=block;strokeColor=#087E81;strokeWidth=2;'+anchors+('dashed=1;' if dashed else ''))
    g=ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
    ET.SubElement(g,'mxPoint',x=str(x1),y=str(y1),attrib={'as':'sourcePoint'});ET.SubElement(g,'mxPoint',x=str(x2),y=str(y2),attrib={'as':'targetPoint'})
    import math
    if dashed:
        n=max(1,int(abs(x2-x1)//18))
        for i in range(0,n,2):d.line((x1+(x2-x1)*i/n,y1+(y2-y1)*i/n,x1+(x2-x1)*(i+1)/n,y1+(y2-y1)*(i+1)/n),fill='#087E81',width=3)
    else:d.line((x1,y1,x2,y2),fill='#087E81',width=3)
    a=math.atan2(y2-y1,x2-x1)
    d.polygon([(x2,y2),(x2-13*math.cos(a-.45),y2-13*math.sin(a-.45)),(x2-13*math.cos(a+.45),y2-13*math.sin(a+.45))],fill='#087E81')
    dash='stroke-dasharray="10 7"' if dashed else ''
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#087E81" stroke-width="3" {dash} marker-end="url(#arrow)"/>')

label('title','Registro de solicitudes SGRA mediante REST',40,20,1320,70,32,True)
label('local','PROTOTIPO LOCAL · Datos ficticios · Khriz Coronel',40,95,1320,45,23,True)
label('client','Cliente externo\nEnvía solicitud individual',50,205,320,120,23,True,True)
label('api','API REST\nValida campos obligatorios',540,205,320,120,23,True,True,fill='#DFEEEB')
label('store','Registro en memoria\nEstado Pendiente',1030,205,320,120,23,True,True)
arrow('request','client','api',370,240,540,240)
label('post','POST + JSON',370,173,170,45,19)
arrow('reply','api','client',540,295,370,295)
label('result','201 + ID / 400',370,325,170,45,19)
arrow('save','api','store',860,265,1030,265)
label('saveLabel','Solo datos válidos',860,202,170,45,18)
label('contract','subjectId · sessionTypeId = 1 · reason · preferredSchedule',50,390,1300,55,23)
label('limit','Sin BD ni sesión real. Reiniciar borra los registros. Reintentar puede duplicarlos.',50,450,1300,45,21)
label('future','EVOLUCIÓN PROPUESTA · Confirmación del último cupo',40,555,1320,55,24,True)
label('nodeA','Nodo A\nAutoridad para confirmar cupos',160,665,400,120,23,True,True)
label('nodeB','Nodo B\nCoordina la misma decisión',840,665,400,120,23,True,True)
arrow('coordination','nodeA','nodeB',560,725,840,725,True)
label('link','Coordinación',565,655,270,40,21)
label('partition','En una partición, suspender la confirmación si no puede garantizarse el cupo único.',40,815,1320,40,22)
label('latency','Sin partición, esperar coordinación añade latencia. Esta topología no está implementada.',40,865,1320,40,21)
out=root/'diagramas';out.mkdir(exist_ok=True)
ET.indent(mxfile,space='  ');ET.ElementTree(mxfile).write(out/'khriz-rest.drawio',encoding='utf-8',xml_declaration=True)
im.save(out/'khriz-rest.png');svg.append('</svg>');(out/'khriz-rest.svg').write_text('\n'.join(svg),encoding='utf-8')

pdf=root/'referencias/fuentes/kazanavicius-mazeika-2023.pdf'
with pdfplumber.open(pdf) as r:
    page=r.pages[2];width,height=page.width,page.height;words=page.extract_words()
    start=next(i for i,w in enumerate(words) if w['text']=='The' and 516<w['top']<518)
    stop=next(i for i in range(start,len(words)) if words[i]['text']=='style.')
    marked=words[start:stop+1]
    buf=BytesIO();overlay=canvas.Canvas(buf,pagesize=(width,height));overlay.setFillColorRGB(1,.9,0);overlay.setFillAlpha(.35)
    for top in sorted({round(w['top'],1) for w in marked}):
        row=[w for w in marked if round(w['top'],1)==top]
        x=min(w['x0'] for w in row);right=max(w['x1'] for w in row);bottom=max(w['bottom'] for w in row)
        overlay.rect(x-1,height-bottom-1,right-x+2,bottom-top+2,stroke=0,fill=1)
    overlay.save();buf.seek(0)
    original=PdfReader(pdf).pages[2];original.merge_page(PdfReader(buf).pages[0]);writer=PdfWriter();writer.add_page(original)
    temp=root/'.analysis-khriz-tmp/articulo-anotado.pdf'
    with temp.open('wb') as f:writer.write(f)
doc=pypdfium2.PdfDocument(str(temp));page=doc[0];bitmap=page.render(scale=2.2);source=bitmap.to_pil().convert('RGB')
sheet=Image.new('RGB',(source.width,source.height+180),'white');sheet.paste(source,(0,90));draw=ImageDraw.Draw(sheet)
draw.text((25,14),'Comunicación síncrona · artículo de 2023 · p. 3',font=font(27,True),fill='#132F3A')
draw.text((25,50),'Kazanavičius y Mažeika · DOI: 10.31577/cai_2023_1_1',font=font(21),fill='#52616A')
draw.text((25,source.height+106),'El cliente espera una respuesta; depende de la disponibilidad del servicio.',font=font(21),fill='#132F3A')
draw.text((25,source.height+142),'Anotación preparada con Codex. Lectura personal de Khriz pendiente.',font=font(20),fill='#52616A')
sheet.save(root/'evidencias/khriz-articulo-comunicacion-anotado.png')
print('Diagramas y captura anotada generados.')
