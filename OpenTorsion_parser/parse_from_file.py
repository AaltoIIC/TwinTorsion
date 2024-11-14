import json
import opentorsion as ot
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from OpenTorsion_parser.parser import parse

file_path = './examples/test-twodisks.tors'

with open(file_path) as input_json:
    input_data = json.load(input_json)
    assembly, excitations = parse(input_data)
    print(excitations)
    plot_tools = ot.Plots(assembly)
    plot_tools.plot_assembly()