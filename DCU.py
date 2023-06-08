# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os
import csv
import sys

def check_duplicates():
    """
    Traverses through given CSV file and puts all
    PDF files into a list so that they can be compared
    in convert()

    :return: list of PDF files without their extension type
    """ 
    current_files = [] #list of current pdf files to skip
    csv_directory = 'csvFolder'
    for filename in os.listdir(csv_directory):
        if filename.endswith('.pdf'): #Ignores pdf files
            new_filename = filename[:-3]
            current_files += [new_filename]
    return current_files     

def switch(key_to_lookup):
    if key_to_lookup == "huntress":
        return "MISSING HUNTRESS AGENT"
    elif key_to_lookup == "sentinelone":
        return "MISSING SENTINEL ONE AGENT"
    elif key_to_lookup == "cybercns-sec-vm":
        return "MISSING CYBERCNS AGENT"
    elif key_to_lookup == "cb-cloud":
        return "MISSING CARBON AGENTS"
    else:
        return "MISSING ALL"
    

def write_Html(file_path, html_buffer, missing):
    set_of_services = {'huntress', 'sentinelone', 'cybercns-sec-vm', 'cb-cloud', 'all'}
    number_of_serverices = 0
    for x in missing:
        if x in set_of_services:
            number_of_serverices+=1
            
    set_of_all = []
    if number_of_serverices > 1:
        frequency = {}
        for service in set_of_services:
            if service in missing:
                for x in missing[service]:
                    if x in frequency:
                        frequency[x] += 1
                    else:
                        frequency[x] = 1
        for names in frequency:
            if frequency[names] == number_of_serverices:
                set_of_all += [names]

    missing['all'] = set_of_all
    with open(os.path.join(file_path, html_buffer), 'w') as Func:
        Func.write("<html>\n<head>\n<title> \nDCUP</title>") #change title when needed
        Func.write("\n<meta hr {display: block; height: 1px; border: 0; border-top: 1px solid #ccc; margin: 1em 0; padding: 0;}>")
        Func.write("\n<style> ")
        Func.write("\nh2 {\nfont-family:  Century Gothic;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np2 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\n.column { float: left; width: 50%;}")
        Func.write("\n{box-sizing: border-box}")
        Func.write("\n.row:after \n{content: \"\"; \ndisplay: table; \nclear: both;}")
        Func.write("</style>")
        for key_to_lookup in missing:
            if key_to_lookup in set_of_services:
                Func.write("\n</h2> <body><h2>" + switch(key_to_lookup) + "</h2><hr>")   # Fill in with whatever needs to be filled
                if not len(missing[key_to_lookup]) == 0: 
                    Func.write("<div class =\"row\">") 
                    Func.write("<div class=\"column\" >") 
                    Func.write("<p>")
                    j=0
                    for x in missing[key_to_lookup]:
                        if not x in set_of_all or key_to_lookup == 'all':
                            if j % 2 == 0:
                                Func.write("\n")
                                Func.write("&bull; ")
                                Func.write(x)
                                Func.write("<br>")
                            j+=1
                    Func.write("</p>")
                    Func.write("</div>") 
                j=0
                Func.write("<div class =\"row\">") 
                Func.write("<div class=\"column\" >") 
                Func.write("<p2><br>")
                if not len(missing[key_to_lookup]) == 0: 
                    for x in missing[key_to_lookup]:
                        if not x in set_of_all or key_to_lookup == 'all':
                            if j % 2 == 1:
                                Func.write("\n")
                                Func.write("&bull; ")
                                Func.write(x)
                                Func.write("<br>")
                            j+=1

                Func.write("</p2>")
                Func.write("</div>") #26
                Func.write("</div>") #22
        Func.write("\n</body></html>") #needs to be last line
        Func.close()
        #DELETE ME 
        #file1.close()

def create_html(f):
    """
    Takes in a CSV file and converts it into
    an HTML file

    :param f: current csv file
    :return: converted html file
    """ 
    #missing_string = find_missing_services(f)
    
    df1 = pd.read_csv(f)
    return df1.to_html() #Converts file to html
    #TODO we can edit the html here

def create_pdf(current_file, html_location):
    """
    Takes in an HTML file and converts it into
    a PDF file

    :param current_file: string name of CSV file
    :param html_file: current HTML file
    """ 
    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe' #Dependency needed for pdfkit
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    #Formats the csv to pdf
    buffer = current_file[:-3]
    pdf_file = buffer + "pdf"
    pdfkit.from_file(html_location, pdf_file, configuration=config)  #Utilizes the pdfkit API to convert the html to a pdf
    os.remove(html_location)

def convert(processed_count, file_path, process_type):
    """
    Traverses through a given directory and searches 
    for CSV files. For each file they are converted
    into PDF files based on the given process type.

    :param processed_count: counts file conversions
    :param file_path: given path to the CSV folder
    :param process_type: Smart, Abort, or Process
    :return: integer of files processed
    """ 
    #file_path = 'csvFolder'

    #Checks for reprocess and smart
    if process_type == 'reprocess':
        current_files = []
    else:
        current_files = check_duplicates()

    # iterate over files in the given directory path
    for filename in os.listdir(file_path):
        buffer_filename = filename[:-3]
        if buffer_filename not in current_files:
            if filename.endswith('.csv'): #Ignores pdf files
                f = os.path.join(file_path, filename)
                if os.path.isfile(f): # checking if it is a file
                    print(filename) #Needed print
                    missing = find_missing_services(f)
                    buffer = filename[:-3]
                    html_buffer = buffer + "html"
                    html_location = file_path + "\\" + html_buffer
                    write_Html(file_path, html_buffer, missing)
                    create_pdf(f, html_location)
                    processed_count+=1
        elif process_type == 'abort':
            print("abort")
            return processed_count
    return processed_count
                

def find_missing_services(csv_file):
    services = {}
    devices = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            device = row[0]
            services_data = row[1:]  # Remaining elements on the line

            devices.append(device)

            for service in services_data:
                if service.strip() != '':
                    services.setdefault(service, []).append(device)

    # List devices missing each service
    dict_missing = {}
    for service, missing_devices in services.items():
        present_devices = set(missing_devices)
        all_devices = set(devices)
        missing = all_devices - present_devices
        dict_missing[service] = missing
        #print(f"Missing devices for service '{service}': {', '.join(sorted(missing))}")
    return dict_missing
    
                               
class CommandLine:
    def __init__(self):
        if len(sys.argv) == 3:
            argument1 = sys.argv[1]
            argument2 = sys.argv[2]
        elif len(sys.argv) == 2:
            argument1 = sys.argv[1]
            argument2 = 'smart'
        else:
            raise Exception("\nMissing at least one argument \nArgument 1 is the path to the CSV file \nArgument 2 is optional and is the processing type")
        convert_counter = 0 #Keeps track of files that have been converted
        convert_counter = convert(convert_counter, argument1, argument2)
        print("{}{}".format(convert_counter, ' files have been converted'))


if __name__ == '__main__':
    app = CommandLine()