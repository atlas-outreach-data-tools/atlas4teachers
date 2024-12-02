import matplotlib.pyplot as plt
import os
import re
import streamlit as st
from code_editor import code_editor
import io
import sys
import json

# Remove restricted modules
for module in ("os", "sys"):
    sys.modules.pop(module, None)

def generate_header_id(header_text):
    """Generate a valid HTML id from the header text by removing special characters."""
    # Convert to lowercase
    header_id = header_text.lower()
    # Replace spaces with hyphens
    header_id = re.sub(r'\s+', '-', header_id)
    # Remove any characters that are not alphanumeric, hyphens, or underscores
    header_id = re.sub(r'[^a-z0-9\-_]', '', header_id)
    return header_id

def insert_toc(content):
    """Generate a floating Table of Contents based on second and third level markdown headers."""
    toc = []
    # Match only second (##) and third (###) level headers
    headers = re.findall(r'^(#{2,3})\s*(.*)', content, re.MULTILINE)
    
    # Only proceed if there are second or third level headers
    if headers:
        # Create a TOC entry for each header
        for level, header_text in headers:
            header_id = generate_header_id(header_text)  # Generate valid HTML id
            if level == '##':
                toc.append(f'<a class="toc-level-2" href="#{header_id}">{header_text}</a>')
            elif level == '###':
                toc.append(f'<a class="toc-level-3" href="#{header_id}">{header_text}</a>')

        # Create the TOC as HTML
        toc_html = """
        <div class="toc">
            <h4>Contents</h4>
            {links}
        </div>
        """.format(links='\n'.join(toc))

        # Inject the TOC into the Streamlit app
        st.markdown(toc_html, unsafe_allow_html=True)

        # Add custom CSS for floating sidebar TOC with a transparent background and different header styles
        st.markdown("""
        <style>
            .toc {
                position: fixed;
                top: 100px;
                right: 20px;
                background-color: rgba(255, 255, 255, 0); /* Transparent background */
                padding: 1rem;
                border-radius: 5px;
                box-shadow: none;
                z-index: 100;
                width: 250px;
                max-height: 70vh;
                overflow-y: auto;
            }
            .toc h4 {
                font-size: 16px;
                margin-bottom: 10px;
            }
            .toc a {
                color: #0366d6;
                text-decoration: none;
                display: block;
                margin-bottom: 8px;
            }
            .toc a:hover {
                text-decoration: underline;
            }
            .toc a.toc-level-2 {
                font-size: 15px;
                font-weight: bold;
                margin-left: 0px; /* No indent for second-level headers */
            }
            .toc a.toc-level-3 {
                font-size: 13px;
                margin-left: 10px; /* Indent for third-level headers */
            }
            /* Allow the TOC to scroll */
            .toc {
                overflow-y: scroll;
            }
        </style>
        """, unsafe_allow_html=True)

def load_markdown_file_with_images(filename, folder, language):
    """Load markdown content, display images with captions, and render text."""
    # Construct the file path based on the selected language
    base_path = f"docs/{language.lower()}/{folder}/{filename}"
    
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Insert Table of Contents (TOC) only if there are second or third level headers
        #insert_toc(content)

        # Parse the content and replace image references
        markdown_buffer = []
        for line in content.splitlines():
            # Search for image markdown syntax ![caption](image_path)
            image_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            
            if image_match:
                # Extract caption and image path
                caption, img_path = image_match.groups()
                # Render the previous markdown content before the image
                if markdown_buffer:
                    st.markdown('\n'.join(markdown_buffer))
                    markdown_buffer = []
                
                # Display the image with caption
                st.image(img_path, caption=caption, width=650)
            else:
                # Add line to the markdown buffer if it's not an image
                markdown_buffer.append(line)

        # Render any remaining markdown content
        if markdown_buffer:
            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)

    else:
        st.error(f"File not found for language: {language}. Check the file path.")

def get_first_level_headers(language, folder, filenames):
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
    Run the code editor in Streamlit with a shared global namespace.
    """
    with open('custom/buttons_code_cells.json') as json_button_file:
        custom_buttons = json.load(json_button_file)

    response_dict = code_editor(
        default_code,
        lang="python",
        # props={"style": {"pointerEvents": "none"}},
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

def load_markdown_file_with_images_and_code(filename, folder, global_namespace, language):
    """Load markdown content, display images, code, and alerts in the correct order."""
    base_path = f"docs/{language.lower()}/{folder}/{filename}"

    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        markdown_buffer = []
        in_code_block = False
        code_buffer = []
        in_alert_block = False
        alert_type = None
        alert_buffer = []
        line_number = 0  # Add a counter for unique keys

        alert_start_re = re.compile(r'> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]')
        alert_end_re = re.compile(r'> \[!END\]')

        for line in content.splitlines():
            line_number += 1  # Increment line number for unique key generation

            if line.startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    # Render any accumulated markdown content before the code block
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                else:
                    in_code_block = False
                    code = '\n'.join(code_buffer)
                    # Pass a unique key to each code editor block
                    run_code_editor(code, global_namespace, key=f"{filename}_line_{line_number}")
                    code_buffer = []
            elif in_code_block:
                code_buffer.append(line)
            elif in_alert_block:
                if alert_end_re.match(line):
                    in_alert_block = False
                    alert_text = '\n'.join(alert_buffer).strip()
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
            else:
                if alert_start_re.match(line):
                    if markdown_buffer:
                        st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                        markdown_buffer = []
                    alert_type = alert_start_re.match(line).group(1)
                    in_alert_block = True
                else:
                    image_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                    if image_match:
                        if markdown_buffer:
                            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)
                            markdown_buffer = []
                        caption, img_path = image_match.groups()
                        st.image(img_path, caption=caption, width=650)
                    else:
                        markdown_buffer.append(line)

        if markdown_buffer:
            st.markdown('\n'.join(markdown_buffer), unsafe_allow_html=True)

    else:
        st.error(f"File not found for language: {language}. Check the file path.")


def load_markdown_preview(filename, folder, language, lines=3):
    # Load the markdown file
    full_path = f"docs/{language.lower()}/{folder}/{filename}"
    with open(full_path, "r") as file:
        content = file.readlines()
    
    # Get the first few lines for the preview
    preview = "".join(content[:lines]).strip()
    return preview

def load_markdown_file_with_dynamic_content_and_alerts(filename, folder, language, **placeholders):
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