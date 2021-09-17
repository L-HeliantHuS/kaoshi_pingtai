#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-09-17
@ FileName: setup_system.py
"""
import os

os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser")