#-*- coding:utf-8 -*-
""" 
All Enrollment from SGA Students
"""
import sys, os, csv
import pyutil
from sga.model import *
sys.path.append(os.getenv('HOME') + '/ddsunl/sga/sgacode/sga-privado/sga')
root = os.path.abspath(os.path.dirname(__file__))

def ejecutar():
    encabezados = ('dni','num.matricula','oferta.academica','fecha','costo',
                   'acreditacion','asistencia/100','carrera','modalidad',
                   'modulo','paralelo','id.paralelo')
    matriculas=Matricula.query.join(['paralelo', 'modulo', 'carrera_programa', 'nivel']).filter(
        ~Nivel.area_siglas.in_(('ACE',))).filter(
        or_(Matricula.estado==EstadoMatriculaAprobada.query.first(), 
            Matricula.estado==EstadoMatriculaMatriculada.query.first(), 
            Matricula.estado==EstadoMatriculaReprobada.query.first())).filter(
            Modulo.carrera_programa!=None).filter(
            Matricula.paralelo!=None).filter(Matricula.papeleta!=None).distinct(
                ).order_by(Matricula.oferta_academica).all()
    nombre_archivo = '%s/enrolments.csv' % root
    f = open(nombre_archivo, mode='wb')
    w = pyutil.UnicodeWriter(f, encoding='ISO-8859-1', delimiter=',',quoting=csv.QUOTE_ALL)
    w.writerow(encabezados)
    datos = [(m.estudiante_cedula,
              str(m.id),
              m.oferta_academica.descripcion,
              str(m.fecha_registro),
              str(m.papeleta.costo_total),
              str(m.promedio_acreditacion),
              str(m.porcentaje_asistencias),
              m.modulo.carrera_programa.nombre if m.modulo.carrera_programa else "sin carrera",
              m.modulo.carrera_programa.modalidad if m.modulo.carrera_programa else "sin modalidad",
              m.modulo.numero,
              m.paralelo.nombre,
              str(m.paralelo.id),
              ) for m in matriculas ]
    # Eliminar repetidos
    datos = set(datos)
    w.writerows(datos)
    f.close()

if __name__ == '__main__':
    ejecutar()
    print 'Script Finalizado !'
