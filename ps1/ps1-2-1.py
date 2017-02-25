# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 23:24:36 2017
@author: Ashish Bajaj
Course: 24-662
PS-1
ps1-2-1
"""
def convert_fahrenheit_to_celcius( temp_in_farenheit ):
    "This function converts temperatures from farenheit to celcius"
    return ((temp_in_farenheit - 32)*(5/9.))
    
def print_temp_in_celcius( temp_in_celcius ):
    "This function prints temperature in celcius"
    print 'It is','%0.02f' %temp_in_celcius,'degrees Celcius.'
    return

def get_temperature_in_farenheit():
    "This function takes the user input of temperature in farenheit"
    return float(input("Enter temperature in Farenheit:"))

def main():
    "Main function"
    farenheit_temperature = get_temperature_in_farenheit()
    celcius_temperature = convert_fahrenheit_to_celcius( farenheit_temperature )
    print_temp_in_celcius(celcius_temperature)
    return

main()