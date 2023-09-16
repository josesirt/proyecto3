# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 21:42:49 2023

@author: ACER
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
from github import Github
from github import InputFileContent
from github.GithubException import GithubException
import inicio
import os
from github import Github
from github import InputFileContent

csv_filename,repo_name,username,access_token,IteradorIris =inicio.comienzo()

class DataAnalyzer:
    def __init__(self, csv_filename):
        self.df = pd.read_csv(csv_filename)

    def calcular_estadisticas(self):
        return self.df.describe()

    def obtener_nombres_variables(self):
        return self.df.columns.tolist()

    def estadisticas_variable(self, nombre_variable):
        if nombre_variable in self.df.columns:
            variable = self.df[nombre_variable].astype(float)
            estadisticas = {
                'Media': variable.mean(),
                'Mediana': variable.median(),
                'Desviación Estándar': variable.std(),
                'Percentil 25': variable.quantile(0.25),
                'Percentil 50': variable.quantile(0.5),
                'Percentil 75': variable.quantile(0.75)
            }
          
            plt.hist(variable, bins=10, edgecolor='k')
            plt.xlabel(nombre_variable)
            plt.ylabel('Frecuencia')
            plt.title(f'Histograma de {nombre_variable}')
            plt.show()
            return estadisticas
        else:
            return "La variable no está disponible en el conjunto de datos."

    def to_dict(self):
        return self.df.to_dict()  # Serializar el DataFrame como un diccionario

if __name__ == "__main__":
    # Crear instancia de la clase IteradorIris
    iterador_iris = IteradorIris(csv_filename)
    for registro in iterador_iris:
        print(registro)

    # Crear instancia de la clase DataAnalyzer
    data_analyzer = DataAnalyzer(csv_filename)
    print("\nEstadísticas generales:")
    print(data_analyzer.calcular_estadisticas())
    
    print("\nNombres de las variables disponibles:")
    print(data_analyzer.obtener_nombres_variables())
    dic = data_analyzer.obtener_nombres_variables()
    con=0
    for d in range(1, len(dic)):
        d=dic[d]
        con=1+con
        print(con)
        if con==5:
            d="Se acabo"
        variable_a_analizar = d # Cambia esto al nombre de la variable que quieras analizar
        print(f"\nEstadísticas de la variable '{variable_a_analizar}':")
        print(data_analyzer.estadisticas_variable(variable_a_analizar))
        
    
    
    
    

try:
    g = Github(access_token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    
    # Serializar iterador_iris y cargarlo como archivo JSON
    iterador_iris_json = json.dumps(list(iterador_iris), indent=4)  # Convertir a JSON
    
    # Verificar si el archivo ya existe en el repositorio
    file_path = "iterador_iris.json"
    filo_path = "data_analyzer.json"
    data_analyzer_json = json.dumps(data_analyzer.to_dict(), indent=4)  # Convertir a JSON
    try:
        existing_file = repo.get_contents(file_path, ref="main")
        repo.update_file(file_path, "Actualización de archivo iterador_iris.json", iterador_iris_json, existing_file.sha, branch="main")
    except Exception:
        # Si el archivo no existe, crearlo
        repo.create_file(file_path, "Creación de archivo iterador_iris.json", iterador_iris_json, branch="main")
    
    
    try:
        existing_file = repo.get_contents(filo_path, ref="main")
        repo.update_file(filo_path, "Actualización de archivo data_analyzer_json", data_analyzer_json, existing_file.sha, branch="main")
    except Exception:
     repo.create_file("data_analyzer.json", "Creación de archivo data_analyzer.json", data_analyzer_json, branch="main")
    
   

    archivos_a_cargar = ["inicio.py", "final.py"]
    for archivo in archivos_a_cargar:
        with open(archivo, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Verificar si el archivo ya existe en el repositorio
        filI_path = archivo
        try:
            existing_file = repo.get_contents(filI_path, ref="main")
            repo.update_file(filI_path, f"Actualización de {archivo}", content, existing_file.sha, branch="main")
            print(f"{archivo} actualizado en GitHub.")
        except Exception:
            repo.create_file(filI_path, f"Creación de {archivo}", content, branch="main")
            print(f"{archivo} creado en GitHub.")
    
    print("Archivos cargados en GitHub correctamente.")
    
  
except Exception as e:
    print(f"Error al cargar archivos en GitHub: {str(e)}")