# Importar
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from textwrap import wrap

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

    # Reemplazar comillas dobles con sencillas
    text = text.replace('"', "'")
    
    # Dividir el texto en lineas
    lineas = text.split('\n')
    
    # Unir las lineas con \n
    textoLimpio = "\\n".join(lineas)
    
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
     
archivo = input("Introduce la ruta del contexto en .txt")
contexto = limpiarTexto(archivo)

pregunta_respuesta(model,contexto,nlp)
