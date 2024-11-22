import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir las variables de entrada
trafico = ctrl.Antecedent(np.arange(0, 301, 1), 'trafico')
hora = ctrl.Antecedent(np.arange(6, 21, 1), 'hora')
lluvia = ctrl.Antecedent(np.arange(0,51,1), 'lluvia')

#Definir la variable de salida
tiempo = ctrl.Consequent(np.arange(1,61,1), 'tiempo')

# Definir las funciones de membresía para las variables de entrada y salida
trafico['bajo'] = fuzz.trapmf(trafico.universe, [0, 0, 0, 100])
trafico['medio'] = fuzz.trimf(trafico.universe, [50, 100, 200])
trafico['alto'] = fuzz.trapmf(trafico.universe, [150, 300, 300,300])

lluvia['ligero'] = fuzz.trapmf(lluvia.universe, [0, 0, 0, 5])
lluvia['normal'] = fuzz.trimf(lluvia.universe, [0, 10, 20])
lluvia['fuerte'] = fuzz.trapmf(lluvia.universe, [15, 50, 50, 50])

hora['manana_temprano'] = fuzz.trapmf(hora.universe, [6, 6, 6, 8])
hora['pico_temprano'] = fuzz.trimf(hora.universe, [7.5, 8, 9])
hora['normal'] = fuzz.trimf(hora.universe, [15, 17, 19])
hora['pico_tarde'] = fuzz.trimf(hora.universe, [8.67, 13, 17.25])
hora['tarde/noche'] = fuzz.trapmf(hora.universe, [18,20, 20,20])

tiempo['corto'] = fuzz.trimf(tiempo.universe, [1, 15, 25])
tiempo['medio'] = fuzz.trimf(tiempo.universe, [20, 30, 45])
tiempo['largo'] = fuzz.trimf(tiempo.universe, [40, 50, 60])


# Definir las reglas difusas
regla1 = ctrl.Rule(trafico['alto'] & lluvia['fuerte'] & hora['pico_tarde'], tiempo['largo'])
regla2 = ctrl.Rule(trafico['medio'] & lluvia['normal'] & hora['manana_temprano'], tiempo['medio'])
regla3 = ctrl.Rule(trafico['bajo'] & lluvia['ligero'] & hora['tarde/noche'], tiempo['corto'])
regla4 = ctrl.Rule(trafico['alto'] & lluvia['ligero'] & hora['pico_tarde'], tiempo['medio'])
regla5 = ctrl.Rule(trafico['medio'] & lluvia['fuerte'] & hora['tarde/noche'], tiempo['largo'])
regla6 = ctrl.Rule(trafico['bajo'] & lluvia['normal'] & hora['normal'], tiempo['corto'])


# Crear el sistema de control difuso
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3,regla4,regla5,regla6])
sistema_control_difuso = ctrl.ControlSystemSimulation(sistema_control)

# Asignar valores de entrada al sistema de control difuso
sistema_control_difuso.input['trafico'] = 75
sistema_control_difuso.input['hora'] = 16.5
sistema_control_difuso.input['lluvia'] = 15


# Activar el sistema de control difuso
sistema_control_difuso.compute()

# Obtener el valor de salida del sistema de control difuso
valor_semaforo = sistema_control_difuso.output['tiempo']

# Mostrar el resultado
print("Valor de tiempo de semáforo:", valor_semaforo)
print("\n\n\n")

# Graficar las funciones de membresía y la salida
trafico.view(sim=sistema_control_difuso)
lluvia.view(sim=sistema_control_difuso)
hora.view(sim=sistema_control_difuso)
tiempo.view(sim=sistema_control_difuso)


plt.show()
