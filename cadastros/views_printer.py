from django.views import View
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
### ------ reportlab imports ------ ###
from reportlab.platypus import Paragraph, Table, TableStyle, LongTable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib import colors
from .printer_data import *

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
                               ('BOTTOMPADDING', (0, 0), (0, -1), 6),

                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),

                               # posições são baseadas matriz
                               # posição M[2][0] até M[2][-1]. -1 faz referencia ao fim
                               ('SPAN', (2, 0), (2, -1)),  # faz o span em uma coluna
                               ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                               ('ALIGN', (4, 0), (4, -1), 'CENTER'),

                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]
                              )

styleTableNormal = [('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),

                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('RIGHTPADDING', (0, 0), (0, -1), 20),
                    ('LEFTPADDING', (1, 0), (1, -1), 20),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]

styleTableReferencia = [('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),
                        ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),

                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),


                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                        ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]


@method_decorator(login_required, name='dispatch')
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
            espaco = Paragraph(f"<br/>", styleErro)
            text = [tabela1, espaco, tabela2, espaco, tabela3]

        elif argumento == "referencias":
            data = printer_referecias()
            tabela = LongTable(data, colWidths=[40, 170, 100, 100, 120])
            tabela.setStyle(styleTableReferencia)
            text.append(tabela)
        else:
            text.append(Paragraph(f"ERRO na geração do documento", styleErro))
        buffer = gerar_doc(text)
        return FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')
