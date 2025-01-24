#
# EPITECH PROJECT, 2024
# main
# File description:
# main
#

import math
import sys

class demography() :
    def __init__(self, pathname, code) :
        self.pathname = pathname
        self.code = code

    def parsing_csv(self, code) :
        file = open(self.pathname, "r")
        for line in file :
            line = line.split(';')
            if line[1] == code :
                return line
        return False

    def str_to_float(self, data) :
        result = [0] * (len(data) - 2)
        for i in range(2, len(data)) :
            result[i - 2] = float(data[i])
        return result

    def print_array(self, data) :
        for i in data :
            print(i)

    def demography_sum(self, data, years) :
        result = [0.0] * 5
        for i in range(len(years)):
            result[0] += float(years[i])                    #x
            result[1] += float(data[i])                     #y
            result[2] += pow(float(years[i]), 2)            #x**2
            result[3] += pow(float(data[i]), 2)             #y**2
            result[4] += float(years[i]) * float(data[i])   #x*y
        return result

    def my_sums(self, data, years) :
        result = [5]
        result = self.demography_sum(data, years)
        return result

    def linear_regression(self, data, years, sums) :
        result = [0.0] * 2
        a = (((len(data) * sums[4]) - (sums[0] * sums[1])) / ((len(data) * sums[2]) - pow(sums[0], 2))) / 1000000
        b = (((sums[1] * sums[2]) - (sums[0] * sums[4])) / ((len(data) * sums[2]) - pow(sums[0], 2))) / 1000000
        result[0] = a
        result[1] = b
        return result

    def linear_regression_years(self, years, data, sums) :
        result = [0.0] * 2
        a = (((len(years) * sums[4]) - (sums[0] * sums[1])) / ((len(years) * sums[2]) - pow(sums[0], 2))) * 1000000
        b = (((sums[1] * sums[2]) - (sums[0] * sums[4])) / ((len(years) * sums[2]) - pow(sums[0], 2)))
        result[0] = a
        result[1] = b
        return result

    def find_RSS(self, a, x, b, data) :
        result = ((data / 1000000) - ((a * x) + b))**2
        return result

    def compute_res_sum(self, data, years, lin_reg) :
        result = 0
        for i in range(len(data)) :
            result += self.find_RSS(lin_reg[0], years[i], lin_reg[1], data[i])
        return result

    def rms_dev(self, data, years, lin_reg) :
        residuate_sum = self.compute_res_sum(data, years, lin_reg)
        result = math.sqrt(residuate_sum / len(data))
        return result

    def find_RSS_x(self, a, y, b, data) :
        result = ((data / 1000000) - ((y - b) / a))**2
        return result

    def compute_res_sum_x(self, data, years, lin_reg) :
        result = 0
        for i in range(len(data)) :
            result += self.find_RSS_x(lin_reg[0], years[i], lin_reg[1], data[i])
        return result

    def rms_dev_x(self, data, years, lin_reg) :
        residuate_sum = self.compute_res_sum_x(data, years, lin_reg)
        result = math.sqrt(residuate_sum / len(data))
        return result

    def find_y_mean(self, data) :
        result = 0
        for i in range(len(data)) :
            result += data[i] / 1000000
        return (result / len(data))

    def find_x_mean(self, years) :
        result = 0
        for i in range(len(years)) :
            result += years[i]
        return (result / len(years))

    def find_TSS(self, data) :
        y_mean = self.find_y_mean(data)
        result = 0
        for i in range(len(data)) :
            result += (data[i] / 1000000 - y_mean)**2
        return result

    def find_ESS(self, data, lin_reg, years) :
        result = 0
        y_mean = self.find_y_mean(data)
        for i in range(len(data)) :
            result = ((((lin_reg[0] * years[i]) + lin_reg[1])) - y_mean)**2
        return result

    def find_upper(self, data, years) :
        result = 0
        x_mean = self.find_x_mean(years)
        y_mean = self.find_y_mean(data)
        for i in range(len(data)) :
            result += ((years[i] - x_mean ) * (data[i] - y_mean))
        return result

    def find_lower_left(self, data, years) :
        result = 0
        x_mean = self.find_x_mean(years)
        for i in range(len(data)) :
            result += (years[i] - x_mean)**2
        return result

    def find_lower_right(self, data) :
        result = 0
        y_mean = self.find_y_mean(data)
        for i in range(len(data)) :
            result += (data[i] - y_mean)**2
        return result

    def find_lower(self, data, years) :
        left = self.find_lower_left(data, years)
        right = self.find_TSS(data)
        result = math.sqrt(left * right)
        return result

    def find_equation(self, data, years) :
        upper = self.find_upper(data, years)
        lower = self.find_lower(data, years)
        result = upper / lower
        return result

    def compute_main(self) :
        data_str = self.parsing_csv(self.code)
        data = self.str_to_float(self.parsing_csv(self.code))
        years = self.str_to_float(self.parsing_csv("Country Code"))
        sums_y = self.my_sums(data, years)
        sums_x = self.my_sums(years, data)
        lin_reg_y = self.linear_regression(data, years, sums_y)
        lin_reg_x = self.linear_regression_years(years, data, sums_x)
        rms_y = self.rms_dev(data, years, lin_reg_y)
        rms_x = self.rms_dev_x(data, years, lin_reg_x)
        prevision_y = (lin_reg_y[0] * 2050) + lin_reg_y[1]
        prevision_x = (2050 - lin_reg_x[1]) / lin_reg_x[0]
        print("Country: " + data_str[0])
        print("Fit1")
        print("\tY = " + str(round(lin_reg_y[0], 2)) + " X ", end='')
        if (lin_reg_y[1] > 0) :
            print("+ ", end='')
            print(str(round(lin_reg_y[1], 2)))
        else :
            print("- ", end='')
            print(str(round((lin_reg_y[1] * -1), 2)))
        print("\tRoot-mean-square deviation: " + str(round(rms_y, 2)))
        print("\tPopulation in 2050: " + str(round(prevision_y, 2)))
        print("\n\n")
        print("Fit2")
        a = round(lin_reg_x[0], 2)
        a_str = f'{a: .2f}'
        print("\tX = {}".format(a_str) + " X ", end='')
        if (lin_reg_x[1] > 0) :
            print("+ ", end='')
            print(str(round(lin_reg_x[1], 2)))
        else :
            print("- ", end='')
            print(str(round((lin_reg_x[1] * -1), 2)))
        print("\tRoot-mean-square deviation: " + str(round(rms_x, 2)))
        print("\tPopulation in 2050: " + str(round(prevision_x, 2)))
        equation = self.find_equation(data, years)
        correlation = equation / 1000000
        correlation_str = f'{correlation: .4f}'
        print(correlation_str)

A = demography("105demography_data.csv", sys.argv[1])
A.compute_main()