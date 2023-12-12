# Importar
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from textwrap import wrap
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#Variables para el modelo
the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
model = AutoModelForQuestionAnswering.from_pretrained(the_model)
nlp = pipeline('question-answering',model=model, tokenizer=tokenizer)

#Función para limpiar texto.
def limpiarTexto(ruta_archivo):
    # Abrir el archivo
    with open(ruta_archivo, 'r') as archivo:
        # Leer el texto del archivo
        text = archivo.read()

    # Replace double quotes with single quotes
    text = text.replace('"', "'")
    
    # Dividir el texto en lineas
    lines = text.split('\n')
    
    # Quitar lineas vacias
    lines = [line for line in lines if line.strip() != '']
    
    # Unir las lineas
    textoLimpio = "\n".join(lines)
    
    return textoLimpio

#Función para preguntas y respuestas
def pregunta_respuesta(model, contexto, nlp):

  #imprimir contexto
  print('Contexto:')
  print('-------------------')
  print('\n'.join(wrap(contexto)))

  #Loop preguntas-respuestas
  continuar = True
  while continuar:
    print('\nPregunta:')
    print('-------------------')
    pregunta = str(input())

    continuar = pregunta!=''

    if continuar:
      salida = nlp({'question':pregunta, 'context':contexto})
      print('\nRespuesta:')
      print('-------------------')
      print(salida['answer'])


os.system('clear')
archivo = input("Introduce la ruta del contexto en .txt: ")
contexto = limpiarTexto(archivo)

pregunta_respuesta(model,contexto,nlp)
