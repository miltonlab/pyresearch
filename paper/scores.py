#-*- coding:utf-8 -*-
""" 
All Enrollment from SGA Students
"""
import sys, os,csv
import pyutil
from sga.model import *
sys.path.append(os.getenv('HOME') + '/ddsunl/sga/sgacode/sga-privado/sga')
root = os.path.abspath(os.path.dirname(__file__))

def ejecutar():
    encabezados = ('dni','id.paralelo','unidad','nota','fecha')
    registros_acreditaciones = RegistroAcreditacion.query.join(['horario_semana']).filter(
        HorarioSemana.jornada!=None).all()
    nombre_archivo = '%s/scores.csv' % root
    f = open(nombre_archivo, mode='wb')
    w = pyutil.UnicodeWriter(f, encoding='ISO-8859-1', delimiter=',',quoting=csv.QUOTE_ALL)
    w.writerow(encabezados)
    datos = [(ra.estudiante_numero_expediente,
              str(ra.horario_semana.jornada.paralelo_id),
              # Prevent "u\201c" and "u\201d" chars and replaza quote chars
              #ra.horario_semana.unidad.nombre.encode('ascii','xmlcharrefreplace').replace('"','\''),
              ra.horario_semana.unidad.nombre.replace(u'\u201c','\'').replace(
                u'\u201d','\'').replace(u'\u2022','?').replace('"','\''),
              str(ra.acreditacion),
              str(ra.fecha),
              ) for ra in registros_acreditaciones ]
    # Eliminar repetidos
    datos = set(datos)
    w.writerows(datos)
    f.close()

if __name__ == '__main__':
    ejecutar()
    print 'Script Finalizado !'
