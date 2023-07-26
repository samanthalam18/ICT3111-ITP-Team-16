import os
import re

# Global variables
DIRS = ['results1/Original','results1/OurModel15','results1/pretrained_Model15','results1/pretrained_Model25','results1/pretrained_Model50']  # Add as many directories as needed
PATTERN = r'(.*)\.png'  # Now matches any filename ending with .png
KEYWORDS = ['Original', 'ourModel','PreModel15','PreModel30','PreModel50']  # Add a keyword for each directory
SIZE = 95

def generate_html(dirs, pattern, keywords):
    # Get the list of image files in each directory
    file_lists = [os.listdir(d) for d in dirs]

    # Create the HTML file
    with open('compare_images.html', 'w') as f:
        # Write the HTML header
        f.write('<html>\n<head>\n<title>Image Comparison</title>\n</head>\n<body>\n')

        # Iterate over the image files in the first directory
        for file in file_lists[0]:
            # Check if the file is an image
            if file.lower().endswith('.png'):
                # Extract the base name of the image
                match = re.match(pattern, file)
                if match:
                    base_name = match.group(1)
                    
                    # Start a new row for each base name
                    f.write(f'<h2>{base_name}</h2>\n')
                    f.write('<div style="display: flex; justify-content: space-around;">\n')
                    
                    # Always add the first image
                    f.write(f'<div style="flex: 1; text-align: center;">\n')
                    f.write(f'<img src="{dirs[0]}/{file}" style="width: {SIZE}%">\n')
                    f.write(f'<p>{keywords[0]}</p>\n')
                    f.write('</div>\n')
                    
                    # Check if a file containing the base name exists in the other directories
                    for i, files in enumerate(file_lists[1:], start=1):
                        matching_files = [f for f in files if base_name in f]
                        if matching_files:
                            # Write the HTML to display the images side by side
                            f.write(f'<div style="flex: 1; text-align: center;">\n')
                            f.write(f'<img src="{dirs[i]}/{matching_files[0]}" style="width: {SIZE}%">\n')
                            f.write(f'<p>{keywords[i]}</p>\n')
                            f.write('</div>\n')
                    
                    f.write('</div>\n')  # End of the row

        # Write the HTML footer
        f.write('</body>\n</html>\n')

# Call the function
generate_html(DIRS, PATTERN, KEYWORDS)
