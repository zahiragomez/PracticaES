def guardar(ruta_archivo, col_x, col_y, rmse):
    with open(ruta_archivo, 'wt') as f:
        f.write(f'{col_x}\n')
        f.write(f'{col_y}\n')
        f.write(f'{rmse}\n')

def cargar(ruta_archivo):
    with open(ruta_archivo, 'rt') as f:
        lines = f.readlines()

    return (lines[0].strip(), lines[1].strip(), float(lines[2].strip()))