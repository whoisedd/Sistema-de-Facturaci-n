#!/usr/bin/env python3
# -*- coding: utf-8 -*-

PRODUCTOS = [
    {"codigo": "C001", "nombre": "Combo 10 Alitas",     "precio": 65,  "stock": 20, "emoji": "🍱"},
    {"codigo": "C002", "nombre": "Combo 20 Alitas",     "precio": 120, "stock": 15, "emoji": "🍱"},
    {"codigo": "C003", "nombre": "Combo Familiar",      "precio": 185, "stock": 10, "emoji": "👨‍👩‍👧‍👦"},
    {"codigo": "B001", "nombre": "Papas Fritas",        "precio": 15,  "stock": 60, "emoji": "🍟"},
    {"codigo": "B002", "nombre": "Aros de Cebolla",     "precio": 18,  "stock": 40, "emoji": "🧅"},
    {"codigo": "B003", "nombre": "Ensalada Coleslaw",   "precio": 12,  "stock": 35, "emoji": "🥗"},
    {"codigo": "D001", "nombre": "Refresco Personal",   "precio": 8,   "stock": 100, "emoji": "🥤"},
    {"codigo": "D002", "nombre": "Jugo Natural",        "precio": 12,  "stock": 50, "emoji": "🧃"},
    {"codigo": "D003", "nombre": "Cerveza",             "precio": 15,  "stock": 80, "emoji": "🍺"},
]


def obtener_productos():
    """Devuelve la lista completa de productos."""
    return PRODUCTOS


def obtener_producto_por_codigo(codigo):
    """Busca un producto por su código. Retorna None si no existe."""
    for p in PRODUCTOS:
        if p["codigo"] == codigo:
            return p
    return None
