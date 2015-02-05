#-*- coding:utf-8 -*-
""" 
All Data Estudiante from SGA
"""
import sys, os, csv
import pyutil
from sga.model import *
sys.path.append(os.getenv('HOME') + '/ddsunl/sga/sgacode/sga-privado/sga')
root = os.path.abspath(os.path.dirname(__file__))

def ejecutar():
    encabezados = ('nombres','apellidos','dni','sexo','pais','ciudad','fecha_nacimiento','email')
    matriculas=Matricula.query.join(Estudiante).join(['paralelo', 'modulo', 'carrera_programa', 'nivel']).filter(
        ~Nivel.area_siglas.in_(('ACE',))).filter(
        or_(Matricula.estado==EstadoMatriculaAprobada.query.first(), 
            Matricula.estado==EstadoMatriculaMatriculada.query.first(), 
            Matricula.estado==EstadoMatriculaReprobada.query.first())).filter(
            Matricula.paralelo_id!=None).distinct().all()
    nombre_archivo = '%s/students.csv' % root
    f = open(nombre_archivo, mode='wb')
    w = pyutil.UnicodeWriter(f, encoding='ISO-8859-1', delimiter=',',quoting=csv.QUOTE_ALL)
    w.writerow(encabezados)
    datos = [(#str(m.id),
              estudiante.nombres.title(),
              estudiante.apellidos.title(),
              estudiante.cedula,
              clasificar_dni(estudiante.cedula),
              estudiante.datos_personales.genero,
              estudiante.datos_personales.pais_procedencia or 'Ecuador',
              estudiante.datos_personales.canton_procedencia or '',
              fecha_nacimiento(estudiante),
              limpiar_email(estudiante.datos_personales.email_institucional) or 
              limpiar_email(estudiante.usuario.email_address) or '%s@unl.edu.ec' % 'no_tiene',
              ) for estudiante in Estudiante.query.filter(Estudiante.expediente!=None).join(['datos_personales']).filter(
            DatosPersonales.genero!=None).filter(Estudiante.usuario!=None).all() ]
    # Eliminar repetidos
    datos = set(datos)
    w.writerows(datos)
    f.close()


def clasificar_dni(dni):
    if len(dni) == 10 and dni.isdigit():
        return 'cedula'
    else:
        return 'pasaporte'

def fecha_nacimiento(e):
    fecha = e.datos_personales.fecha_nacimiento
    # Ciertas fechas erroneas
    if fecha and fecha.year >= 1900:
        return fecha.strftime('%d/%m/%Y')
    else:
        return ""

def limpiar_email(email):
    if email:
        # Cierto caracter especial presente en un correo
        return email.replace(u'\u2022','')
    else:
        return ""

if __name__ == '__main__':
    ejecutar()
    print 'Script Finalizado !'
