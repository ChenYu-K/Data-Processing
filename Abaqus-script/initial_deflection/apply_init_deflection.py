import numpy as np

def read_nodes_from_inp(filename, part_name):
    nodes = []
    original_lines = []
    inside_part = False
    with open(filename, 'r') as file:
        for line in file:
            original_lines.append(line)
            line = line.strip()
            if line.startswith('*'):
                if line.startswith('*Part') and f'name={part_name}' in line:
                    inside_part = True
                elif inside_part:
                    if line.startswith('*Node'):
                        continue
                    elif line.startswith('*'):
                        inside_part = False
            elif inside_part and line:
                if ',' in line:
                    node_data = line.split(',')
                    node_id = int(node_data[0].strip())
                    x = float(node_data[1].strip())
                    y = float(node_data[2].strip())
                    z = float(node_data[3].strip())
                    nodes.append((node_id, x, y, z))
    return nodes, original_lines

def write_nodes_to_inp(filename, original_lines, deflected_nodes, part_name):
    deflected_dict = {node[0]: node for node in deflected_nodes}
    inside_part = False
    inside_node = False
    with open(filename, 'w') as file:
        for line in original_lines:
            stripped_line = line.strip()
            if stripped_line.startswith('*'):
                if stripped_line.startswith('*Part') and f'name={part_name}' in stripped_line:
                    inside_part = True
                elif inside_part and stripped_line.startswith('*Node'):
                    inside_node = True
                elif inside_part and stripped_line.startswith('*'):
                    inside_part = False
                    inside_node = False

            if inside_node and ',' in stripped_line:
                node_data = stripped_line.split(',')
                node_id = int(node_data[0].strip())
                if node_id in deflected_dict:
                    x, y, z = deflected_dict[node_id][1:]
                    file.write(f'      {node_id}, {x:.6f}, {y:.6f}, {z:.6f}\n')
                else:
                    file.write(line)
            else:
                file.write(line)

# 定义初期形变函数
def init_defle(A, a, b, x, y):
    import numpy as np
    defle = a / A * np.sin(np.pi * x / a) * np.sin(np.pi * y / b)
    return defle

# 添加形变到节点数据
def add_deflection(nodes, A, a, b, origin):
    deflected_nodes = []
    for node_id, x, y, z in nodes:
        if origin[1] <= y <= origin[2] and min(origin[3],origin[4]) <= z <= max(origin[3],origin[4]):
            norm_y = abs(y - origin[1])
            norm_z = abs(z - origin[3])
            deflection = init_defle(A, a, b, norm_y, norm_z)
            deflected_nodes.append((node_id, x + deflection, y, z))
        else:
            deflected_nodes.append((node_id, x, y, z))
    return deflected_nodes

# 添加形变到节点数据to flange-1
def add_def_xp1(nodes, A, a, b, origin):
    deflected_nodes = []
    for node_id, x, y, z in nodes:
        if origin[1] <= y <= origin[2] and min(origin[3],origin[4]) <= z <= max(origin[3],origin[4]):
            norm_y = abs(y - origin[1])
            norm_z = abs(z - origin[3])
            deflection = init_defle(A, a, b, norm_y, norm_z)
            deflected_nodes.append((node_id, x, y - deflection, z))
        else:
            deflected_nodes.append((node_id, x, y, z))
    return deflected_nodes