import matplotlib.pyplot as plt
import os
import re
import streamlit as st
from code_editor import code_editor
import io
import sys
import json

def generate_header_id(header_text):
    """
    Generate a valid HTML id from the header text by removing special characters.

    1. Lowercase Conversion: Converts the entire header text to lowercase.
    2. Whitespace Replacement: Replaces all whitespace characters with hyphens ('-').
    3. Special Character Removal: Removes any characters that are not alphanumeric, hyphens, or underscores.

    Parameters:
        header_text (str): The original header text that needs to be converted into a valid HTML id.

    Returns:
        str: A sanitized, lowercase string with hyphens replacing spaces and all other special characters removed,
             suitable for use as an HTML id.
    """
    # Convert to lowercase
    header_id = header_text.lower()
    # Replace spaces with hyphens
    header_id = re.sub(r'\s+', '-', header_id)
    # Remove any characters that are not alphanumeric, hyphens, or underscores
    header_id = re.sub(r'[^a-z0-9\-_]', '', header_id)
    return header_id

def get_first_level_headers(language, folder, filenames):
    """
    Extract the first-level markdown header (# ) from each file.

    Reads files from "docs/{language}/{folder}/", retrieves the first line starting with '# ',
    and returns a list of the header texts. Prints an error if a file is not found.

    Parameters:
        language (str): Language code (used in lowercase for the path).
        folder (str): Folder name containing the files.
        filenames (list): List of file names.

    Returns:
        list: First-level headers from each file.
    """
    headers = []
    for filename in filenames:
        base_path = f"docs/{language.lower()}/{folder}/{filename}"
        try:
            with open(base_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('# '):
                        header = line.strip('# ').strip()
                        headers.append(header)
                        break  # Stop after the first header is found
        except FileNotFoundError:
            print(f"File not found: {base_path}")
    return headers

def run_code_editor(default_code, global_namespace, height=[2,30], key=None):
    """
    Launch a Streamlit code editor, execute submitted Python code, and display output.

    Loads custom buttons from a JSON file and opens a code editor with the given default code.
    When the user submits code, it is executed in the provided global namespace. Captured
    standard output and any generated matplotlib figures are then displayed.

    Parameters:
        default_code (str): The initial code shown in the editor.
        global_namespace (dict): The namespace in which the submitted code is executed.
        height (list, optional): A two-element list defining the editor's height.
        key (str, optional): A unique key for the editor widget.

    Returns:
        None
    """
    with open('custom/buttons_code_cells.json') as json_button_file:
        custom_buttons = json.load(json_button_file)

    response_dict = code_editor(
        default_code,
        lang="python",
        props={"style": {"pointerEvents": "none"}},
        height=height,
        theme="monokai",
        buttons=custom_buttons,
        key=key  # Add a unique key here
    )

    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            exec(code, global_namespace)
        except IndentationError as e:
            st.error(f"Indentation Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

        output = buffer.getvalue()
        if output:
            st.code(output, language="python")

        sys.stdout = old_stdout

        if plt.get_fignums():
            st.pyplot(plt.gcf())
            plt.close('all')

def load_markdown_preview(filename, folder, language, lines=3):
    """
    Load a markdown file and return a preview of its first few lines.
    
    Parameters:
        filename (str): Name of the markdown file.
        folder (str): Folder containing the file.
        language (str): Language folder name (converted to lowercase).
        lines (int, optional): Number of lines to include in the preview (default is 3).
    
    Returns:
        str: Preview text from the file.
    """
    # Load the markdown file
    full_path = f"docs/{language.lower()}/{folder}/{filename}"
    with open(full_path, "r") as file:
        content = file.readlines()
    
    # Get the first few lines for the preview
    preview = "".join(content[:lines]).strip()
    return preview

def load_markdown_file_combined(filename, folder, language, global_namespace=None, **placeholders):
    """
    Load markdown content from a file and process dynamic content, images, code blocks,
    alerts, and dataframe blocks based on the file's content.

    Parameters:
        - filename: The markdown file name.
        - folder: The folder in which the file is stored.
        - language: The language sub-folder.
        - global_namespace: Optional. If provided, code blocks will be executed via run_code_editor.
        - placeholders: Optional keyword arguments for dynamic placeholder replacement.
    """
    base_path = f"docs/{language.lower()}/{folder}/{filename}"
    
    if not os.path.exists(base_path):
        st.error(f"File not found: {base_path}")
        return

    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace dynamic placeholders if any
    for key, value in placeholders.items():
        content = content.replace(f"{{{key}}}", str(value))
    
    # Initialize buffers and flags
    markdown_buffer = []
    in_code_block = False
    code_buffer = []
    in_alert_block = False
    alert_type = None
    alert_buffer = []
    in_dataframe_block = False
    dataframe_var = None  # The key for the dataframe in placeholders
    line_number = 0  # For generating unique keys for code blocks

    # Regular expressions for different markers
    alert_start_re = re.compile(r'> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]')
    alert_end_re = re.compile(r'> \[!END\]')
    dataframe_start_re = re.compile(r'> \[!dataframe\]')
    dataframe_end_re = re.compile(r'> \[!end\]')
    image_re = re.compile(r'!\[(.*?)\]\((.*?)\)')

    # Process the file line by line
    for line in content.splitlines():
        line_number += 1

        # --- Code Block Handling ---
        if line.startswith("```"):
            if not in_code_block:
                # Start of a code block
                in_code_block = True
                # Render any pending markdown before starting the code block
                if markdown_buffer:
                    st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                    markdown_buffer = []
            else:
                # End of a code block
                in_code_block = False
                code = '\n'.join(code_buffer)
                if global_namespace is not None:
                    run_code_editor(code, global_namespace, key=f"{filename}_line_{line_number}")
                code_buffer = []
            continue  # Skip further processing for this line

        if in_code_block:
            code_buffer.append(line)
            continue

        # --- Dataframe Block Handling ---
        if in_dataframe_block:
            if dataframe_end_re.match(line):
                in_dataframe_block = False
                if dataframe_var and dataframe_var in placeholders:
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                    st.dataframe(placeholders[dataframe_var])
                dataframe_var = None
            else:
                # Assume the line inside a dataframe block is the key for the dataframe
                dataframe_var = line.strip()
            continue

        if dataframe_start_re.match(line):
            in_dataframe_block = True
            continue

        # --- Alert Block Handling ---
        if in_alert_block:
            if alert_end_re.match(line):
                in_alert_block = False
                alert_text = '\n'.join(alert_buffer).strip()
                # Display the alert based on its type
                if alert_type == "NOTE":
                    st.info(alert_text)
                elif alert_type == "TIP":
                    st.success(alert_text)
                elif alert_type == "IMPORTANT":
                    st.warning(alert_text)
                elif alert_type == "WARNING":
                    st.error(alert_text)
                elif alert_type == "CAUTION":
                    st.warning(alert_text)
                alert_buffer = []
            else:
                alert_buffer.append(line)
            continue

        if alert_start_re.match(line):
            # Flush pending markdown before starting an alert block
            if markdown_buffer:
                st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                markdown_buffer = []
            alert_type = alert_start_re.match(line).group(1)
            in_alert_block = True
            continue

        # --- Image Handling ---
        if image_re.match(line):
            image_match = image_re.match(line)
            if image_match:
                # Flush pending markdown before displaying an image
                if markdown_buffer:
                    st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                    markdown_buffer = []
                caption, img_path = image_match.groups()
                st.image(img_path, caption=caption, width=650)
            continue

        # --- Accumulate Markdown ---
        markdown_buffer.append(line)

    # Render any remaining markdown content
    if markdown_buffer:
        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
    """Load markdown content, replace placeholders, handle alerts and images, and render dynamically."""
    base_path = f"docs/{language.lower()}/{folder}/{filename}"

    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace placeholders with dynamic values
        for key, value in placeholders.items():
            content = content.replace(f"{{{key}}}", str(value))

        markdown_buffer = []
        in_alert_block = False
        alert_type = None
        alert_buffer = []
        in_dataframe_block = False  # Track dataframe blocks
        line_number = 0  # For unique keys

        # Alert regex patterns
        alert_start_re = re.compile(r'> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]')
        alert_end_re = re.compile(r'> \[!END\]')

        dataframe_start_re = re.compile(r'> \[!dataframe\]')
        dataframe_end_re = re.compile(r'> \[!end\]')

        for line in content.splitlines():
            line_number += 1

            # Handle dataframe blocks block to determine if dataframe
            if in_dataframe_block:
                if dataframe_end_re.match(line):
                    in_dataframe_block = False
                    if dataframe_var and dataframe_var in placeholders:
                        if markdown_buffer:
                            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                            markdown_buffer = []
                        st.dataframe(placeholders[dataframe_var])  # Render the dataframe
                    dataframe_var = None
                else:
                    dataframe_var = line.strip()
            elif dataframe_start_re.match(line):
                in_dataframe_block = True
            
            # Handle alerts
            elif in_alert_block:
                if alert_end_re.match(line):
                    in_alert_block = False
                    alert_text = '\n'.join(alert_buffer).strip()
                    # Display the alert based on its type
                    if alert_type == "NOTE":
                        st.info(alert_text)
                    elif alert_type == "TIP":
                        st.success(alert_text)
                    elif alert_type == "IMPORTANT":
                        st.warning(alert_text)
                    elif alert_type == "WARNING":
                        st.error(alert_text)
                    elif alert_type == "CAUTION":
                        st.warning(alert_text)
                    alert_buffer = []
                else:
                    alert_buffer.append(line)
            elif alert_start_re.match(line):
                if markdown_buffer:
                    st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                    markdown_buffer = []
                alert_type = alert_start_re.match(line).group(1)
                in_alert_block = True

            # Handle images
            elif re.match(r'!\[(.*?)\]\((.*?)\)', line):
                image_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                if image_match:
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                    caption, img_path = image_match.groups()
                    st.image(img_path, caption=caption, width=650)
            
            # Buffer markdown
            else:
                markdown_buffer.append(line)

        # Render any remaining markdown content
        if markdown_buffer:
            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)

    else:
        st.error(f"File not found: {base_path}")