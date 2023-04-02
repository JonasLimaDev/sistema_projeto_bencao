from django.views import View
from django.http import FileResponse

### ------ reportlab imports ------ ###
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib import colors
from .printer_data import *
from .services import gerar_doc

styles = getSampleStyleSheet()
set_fonts()
styleErro = ParagraphStyle('erro',
                           fontSize=20,
                           parent=styles['Normal'],
                           alignment=1,
                           spaceBefore=0,
                           spaceAfter=14)
styleTableBairro = TableStyle([('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('FONTNAME', (0,0), (-1,0), 'ArialN'),

                               # posições são baseadas matriz
                               # posição M[2][0] até M[2][-1]. -1 faz referencia ao fim
                               ('SPAN', (2, 0), (2, -1)),  # faz o span em uma coluna
                               ('SPAN', (5, 0), (5, -1)),


                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]
                              )
styleTableNormal = TableStyle([('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('FONTNAME', (0,0), (-1,0), 'ArialN'),
                               ('FONTNAME', (0, 1), (-1, -1), 'Arial'),

                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('RIGHTPADDING', (0, 0), (0, -1), 20),
                               ('LEFTPADDING', (1, 0), (1, -1), 20),
                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]
                              )


class PrinterTableView(View):
    def get(self, request, *args, **kwargs):
        argumento = self.kwargs['filter']
        print(argumento)
        data = []
        text = []
        if argumento == "por_bairros":
            data = printer_total_bairro()
            tabela = Table(data)
            tabela.setStyle(styleTableBairro)
            text.append(tabela)
        elif argumento == "por_ruc":
            data = printer_total_ruc()
            tabela = Table(data)
            tabela.setStyle(styleTableNormal)
            text.append(tabela)
        elif argumento == "por_cras":
            data = printer_total_cras()
            tabela = Table(data)
            tabela.setStyle(styleTableNormal)
            text.append(tabela)
        elif argumento == "tudo":
            data1 = printer_total_bairro()
            data2 = printer_total_ruc()
            data3 = printer_total_cras()

            tabela1 = Table(data1)
            tabela2 = Table(data2)
            tabela3 = Table(data3)
            tabela1.setStyle(styleTableBairro)
            tabela2.setStyle(styleTableNormal)
            tabela3.setStyle(styleTableNormal)
            espaco =Paragraph(f"<br/>", styleErro)
            text = [tabela1,espaco,tabela2,espaco,tabela3]
        else:
            text.append(Paragraph(f"ERRO na geração do documento", styleErro))
        buffer = gerar_doc(text)
        return FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')
