#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Скрипт для построения графиков функций вида F(x, y) = 0.
#
# Данная реализация крайне неэффективна и не предназначена для использования в реальных расчетах.
#

from math import *

# Принимает параметры для построения сетки (область и шаг по двум кооринатам),
# возвращает узлы сетки как список точек.
def grid(x_min, x_max, x_step, y_min, y_max, y_step):

	from itertools import count, takewhile

	# Реализация функции range для работы с дробными интервалами.
	def drange(start, stop, step):
	    return takewhile(lambda x: x <= stop, count(start, step))

	result = []
	for x in drange(x_min, x_max, x_step):
		for y in drange(y_min, y_max, y_step):
			point = (x, y)
			result.append(point)
	return result

#
# Функция для численного решения уравнений вида F(x, y) = 0. 
# Возвращает список узлов сетки, являющихся решением уравнения.
#
# F - функция от двух переменных.
#
# accuracy - точность - если модуль значения функции в некоторой точке меньше точности, 
# считаем что функция равна нулю в данной точке. Рекомендуемое значение точности - половина шага сетки.
#
def solve(F, accuracy, grid):

	# Функция определяющая является ли данная точка решением уравнения с точностью accuracy.
	def eq(F, x, y, accuracy):
		try:
			return abs(F(x, y)) < accuracy
		except ValueError as e:
			return False

	result = []
	for p in grid:
		x = p[0]; y = p[1]
		if eq(F, x, y, accuracy):
			result.append(p)
	return result

#
# Функция принимает массив точек и строит график соответствующей функции.
# Поскольку на форму графика влияет порядок отрисовки точек, 
# каждая четверть графика отрисовывается отдельно, с сортировкой точек по одной из координат.
#
def plot(points):
	
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_title('Plot of implicitly defined equation')
	pp = sorted([(p[0], p[1]) for p in points if p[0] >= 0 and p[1] >= 0],key=lambda p: p[0])
	pn = sorted([(p[0], p[1]) for p in points if p[0] >= 0 and p[1] <= 0],key=lambda p: p[0])
	nn = sorted([(p[0], p[1]) for p in points if p[0] <= 0 and p[1] <= 0],key=lambda p: p[0])
	np = sorted([(p[0], p[1]) for p in points if p[0] <= 0 and p[1] >= 0],key=lambda p: p[0])
	plt.plot(*zip(*pp))
	plt.plot(*zip(*pn))
	plt.plot(*zip(*nn))
	plt.plot(*zip(*np))
	plt.show()

# Пример использования.
def main():
	
	# Функция график которой нужно построить.
	F = lambda x, y: y ** 2 + x ** 2 - 1
	# Сетка на которой будет численно решаться уравнение.
	GRID = grid(-1, 1, 0.01, -1, 1, 0.01)
	# Точки - решения уравнения.
	results = solve(F, 0.005, GRID)
	# Печать результатов решения.
	for result in results: print(result)
	# Отрисовка графика.
	plot(results)

if __name__ == '__main__':
	main()
