#! /usr/bin/python

import subprocess
from prettytable import PrettyTable

result = subprocess.run(['pacman', '-Qi'], stdout=subprocess.PIPE)
file_content = result.stdout.decode("utf-8")

packages = file_content.split("\n\n")

package_dict = {}
size_dict = {}

total_size = 0

for package in packages:
    
    name = None
    size = None

    split_line = package.splitlines()
    for line in split_line:
        if "Name" in line:
            name = line.split(":")[1]
        if "Installed Size" in line:
            size = line.split(":")[1].strip()
            
            if "KiB" in size:
                size = size.split()[0]
            if "MiB" in size:
                size = str((float(size.split()[0]) * 1024))
            if "GiB" in size:
                size = str((float(size.split()[0]) * 1024 * 1024))
            if "B" in size:
                size = str((float(size.split()[0]) / 1024))


            size_dict[name] = float(size)
            total_size += float(size) / 1024

sorted_dict = {}
for key in sorted(size_dict, key=size_dict.get):
    sorted_dict[key] = size_dict[key]

table = PrettyTable()
table.field_names = ['package', 'size (MB)']
table.align = 'l'

for i in reversed(sorted_dict.items()):
    table.add_row([i[0], round(i[1] / 1024, 2)])

print(table, '\n')

print("Total Installed Size:", round(total_size, 2), "MB")
