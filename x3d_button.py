import os
import argparse
import shutil

parser = argparse.ArgumentParser(
    prog='X3D button creation in HTML file',
    description='Copies X3D files from input folder to output folder and injects buttons into an HTML file.',
    epilog='Text at the bottom of help'
)

parser.add_argument(
    '-i', '--input-folder',
    required=True,
    help='Path to the folder containing files to be processed'
)

parser.add_argument(
    '-o', '--output-folder',
    required=True,
    help='Path to the destination folder where files will be copied'
)

parser.add_argument(
    '-H', '--html-file',
    required=True,
    help='Path to the HTML file to modify'
)

args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder
html_file_path = args.html_file

os.makedirs(output_folder, exist_ok=True)

file_list = [name for name in os.listdir(input_folder) if name.endswith('.x3d')]

for file_name in file_list:
    src = os.path.join(input_folder, file_name)
    dst = os.path.join(output_folder, file_name)
    if not os.path.exists(dst):
        shutil.copy2(src, dst)

temp_file_path = html_file_path + '.tmp'

with open(html_file_path, 'r') as file_input, \
     open(temp_file_path, 'w') as file_output:

    for line in file_input:
        file_output.write(line)
        
        if 'PRAGMA1' in line:
            file_output.write('<group id="switches">\n')
            for file_name in file_list:
                base = os.path.splitext(file_name)[0].replace('(', '').replace(')', '').replace(' ', '_')
                file_output.write(f'   <switch id="{base}" whichChoice="-1">\n')
                file_output.write(f'       <inline id="{base}" url="assets/{file_name}"></inline>\n')
                file_output.write('   </switch>\n')
            file_output.write('</group>\n')

        if 'PRAGMA2' in line:
            file_output.write('<div class="controls">\n')
            for file_name in file_list:
                base = os.path.splitext(file_name)[0].replace('(', '').replace(')', '').replace(' ', '_')
                file_output.write(
                    f'   <button id="{base}Btn" data-visible="false" '
                    f'onclick="toggleVisibility(\'{base}Btn\', \'{base}\')"> Toggle {base}</button>\n'
                )
            file_output.write('</div>\n')

os.replace(temp_file_path, html_file_path)

print(f"HTML file '{html_file_path}' updated successfully.")
print(f"Copied {len(file_list)} X3D files to '{output_folder}'.")
