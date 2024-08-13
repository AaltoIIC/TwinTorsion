import opentorsion as ot
import argparse
import json

def add_element(element_dict, disk_list, shaft_list, gear_list, i, prev_element=None):
    """
    Add element to the list corresponding to its type
    """
    if element_dict['type'] == 'Disk':
        current_elem = ot.Disk(i, I=element_dict['inertia'], c=element_dict['damping'])
        disk_list.append(current_elem)
        i+=1
    
    elif element_dict['type'] == 'ShaftDiscrete':
        current_elem = ot.Shaft(i-1, i, k=element_dict['stiffness'], c=element_dict['damping'])
        shaft_list.append(current_elem)
    
    elif element_dict['type'] == 'GearElement':
        # if previous element is a gear as well, make it parent of current one

        # gear_length is either radius or number of teeth
        gear_length = element_dict['teeth'] if 'teeth' in element_dict else element_dict['radius'] 

        if prev_element and isinstance(prev_element, ot.Gear):
            current_elem = ot.Gear(i, I=element_dict['inertia'], R=gear_length, parent=prev_element)
        else:
            current_elem = ot.Gear(i, I=element_dict['inertia'], R=gear_length)
        
        gear_list.append(current_elem)
        i+=1
    
    return (i, current_elem)

def add_component(component, disk_list, shaft_list, gear_list, i, prev_element=None):
    """
    Go through elements of component and add them
    """
    for element_dict in component["elements"]:
        i, prev_element = add_element(element_dict, disk_list, shaft_list, gear_list, i, prev_element)

    return (i, prev_element)

def find_component(component_name, components):
    """
    Find component based on name
    """
    for component in components:
        if component["name"] == component_name:
            return component

# returns a dictionary of connections from structure
# ASSUMES EACH COMPONENT HAS ONE SOURCE AND ONE TARGET CONNECTION
def structure_to_dict(structure):
    connections = {}
    for connection in structure:
        connections[connection[0].split('.')[0]] = connection[1].split('.')[0]
    return connections

# returns an OpenTorsion assembly object of the system in the JSON file
def parse(input_data):
        
    # get the list of components
    structure = structure_to_dict(input_data['structure'])
    first_component = (set(structure.keys()) - set(structure.values())).pop()
    list_of_components = [first_component]
    while True:
        next_component = structure[list_of_components[-1]]
        list_of_components.append(next_component)
        if next_component not in structure.keys():
            break
    
    # go through components and add them
    disk_list, shaft_list, gear_list = [], [], []
    i = 0
    prev_element = None
    for component_name in list_of_components:
        component = find_component(component_name, input_data['components'])
        i, prev_element = add_component(component, disk_list, shaft_list, gear_list, i, prev_element)
    
    # creating the assembly object
    if gear_list: # if gear_list is not empty
        assembly = ot.Assembly(shaft_list, disk_elements=disk_list, gear_elements=gear_list)
    else:
        assembly = ot.Assembly(shaft_list, disk_elements=disk_list)
    
    return assembly

def plot_assembly(assembly):
    plot_tools = ot.Plots(assembly)
    plot_tools.plot_assembly()

def main():
    arg_parser = argparse.ArgumentParser(description="Process a JSON file path.")
    arg_parser.add_argument('json_file', type=str, help='Path to the JSON file')
    json_path = arg_parser.parse_args().json_file

    assert json_path

    with open(json_path) as input_json:
        input_data = json.load(input_json)
        parse(input_data)
        #plot_assembly(parse(input_data))

if __name__=='__main__':
    main()