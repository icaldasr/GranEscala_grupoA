def obtener_consultorios(_consulta):
    contador = 0
    consultorios = list()
    temp = _consulta[0][0]
    consultorios.append(temp)
    while contador < len(_consulta):
        if _consulta[contador][0] != temp:
            temp = _consulta[contador][0]
            consultorios.append(temp)
        contador = contador + 1
    return consultorios



