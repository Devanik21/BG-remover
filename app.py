import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from io import BytesIO
import base64
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Advanced Background Remover",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
def load_css():
    """Loads custom CSS for styling the app, focusing on a dark mode theme."""
    st.markdown("""
    <style>
        /* --- General App Styling --- */
        .stApp {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }

        /* --- Sidebar Styling --- */
        .css-1d391kg {
            background-color: #2a2a2e;
            border-right: 2px solid #4a4a4a;
        }
        
        .css-1d391kg .st-emotion-cache-16txtl3 {
            color: #FAFAFA;
        }

        /* --- Main Content Styling --- */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        /* --- Title and Header Styling --- */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            color: #FFFFFF;
            font-weight: 700;
        }

        h1 {
            border-bottom: 3px solid #00A3FF;
            padding-bottom: 10px;
            text-align: center;
        }

        /* --- Button and Widget Styling --- */
        .stButton>button {
            border-radius: 20px;
            border: 2px solid #00A3FF;
            background-color: transparent;
            color: #00A3FF;
            padding: 10px 25px;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #00A3FF;
            color: #1E1E1E;
            border-color: #00A3FF;
            box-shadow: 0 0 15px #00A3FF;
        }
        
        .stDownloadButton>button {
             border-radius: 20px;
            border: 2px solid #28a745;
            background-color: #28a745;
            color: white;
            padding: 10px 25px;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
            width: 100%;
        }

        .stDownloadButton>button:hover {
            background-color: #218838;
            color: white;
            border-color: #1e7e34;
        }

        /* --- File Uploader Styling --- */
        .stFileUploader {
            border: 2px dashed #4a4a4a;
            border-radius: 15px;
            padding: 20px;
            background-color: #2a2a2e;
        }

        .stFileUploader label {
            color: #FAFAFA;
            font-size: 1.1em;
        }
        
        /* --- Expander/Accordion Styling --- */
        .stExpander {
            border: 1px solid #4a4a4a;
            border-radius: 10px;
            background-color: #2a2a2e;
        }
        
        .stExpander header {
            font-weight: bold;
            color: #00A3FF;
        }

        /* --- Image Card Styling --- */
        .image-container {
            background-color: #2a2a2e;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #4a4a4a;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        
        .image-container:hover {
            transform: scale(1.02);
        }

        .image-container img {
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
        
        .image-caption {
            font-size: 1.1em;
            margin-top: 15px;
            color: #FAFAFA;
            font-weight: bold;
        }

    </style>
    """, unsafe_allow_html=True)


# --- Constants ---
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB
MAX_IMAGE_DIM = 2500  # pixels

# --- Core Image Processing Functions ---

def convert_image_to_bytes(img, format="PNG"):
    """Converts a PIL Image to a byte buffer."""
    buf = BytesIO()
    img.save(buf, format=format)
    byte_im = buf.getvalue()
    return byte_im

def resize_image(image, max_dim=MAX_IMAGE_DIM):
    """Resizes an image proportionally to a maximum dimension."""
    width, height = image.size
    if width <= max_dim and height <= max_dim:
        return image
    
    aspect_ratio = width / height
    if width > height:
        new_width = max_dim
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_dim
        new_width = int(new_height * aspect_ratio)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

@st.cache_data(ttl=3600, show_spinner="Processing your image...")
def process_image(image_bytes, session_options):
    """
    Processes the image using rembg and applies selected enhancements.
    This function is cached to speed up repeated operations.
    """
    try:
        original_image = Image.open(BytesIO(image_bytes))
        
        # Ensure image is in RGBA format for processing
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')

        # Resize large images before heavy processing
        resized_image = resize_image(original_image, MAX_IMAGE_DIM)

        # Apply pre-processing filters if enabled
        processed_image = resized_image
        if session_options['use_sharpen']:
            processed_image = processed_image.filter(ImageFilter.SHARPEN)
        if session_options['use_contrast']:
            enhancer = ImageEnhance.Contrast(processed_image)
            processed_image = enhancer.enhance(1.2) # Enhance contrast by 20%

        # Core background removal
        # The rembg parameters can be exposed to the user in the UI
        removed_bg_image = remove(
            processed_image,
            alpha_matting=session_options['alpha_matting'],
            alpha_matting_foreground_threshold=session_options['fg_threshold'],
            alpha_matting_background_threshold=session_options['bg_threshold']
        )
        
        # Post-processing: Add a custom background color
        if session_options['bg_color'] != 'transparent':
            bg_image = Image.new("RGBA", removed_bg_image.size, session_options['bg_color'])
            bg_image.paste(removed_bg_image, (0, 0), removed_bg_image)
            final_image = bg_image.convert("RGB") # Convert to RGB if bg is solid
        else:
            final_image = removed_bg_image

        return resized_image, final_image
    
    except Exception as e:
        st.error(f"Error during image processing: {str(e)}")
        # Optionally log the full traceback for debugging
        # import traceback
        # print(traceback.format_exc())
        return None, None

def display_image_card(image, caption, key_prefix):
    """Creates a styled card to display an image."""
    st.markdown(f'<div class="image-container">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown(f'<p class="image-caption">{caption}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Application UI ---
def main():
    load_css()
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h1>⚙️ Controls</h1>", unsafe_allow_html=True)
        st.markdown("---")

        my_upload = st.file_uploader(
            "Upload your image",
            type=["png", "jpg", "jpeg"],
            help=f"Max file size: {MAX_FILE_SIZE/1024/1024:.0f}MB"
        )
        st.markdown("---")
        
        st.markdown("<h3>Processing Options</h3>", unsafe_allow_html=True)
        
        # Use session state to hold options
        if 'session_options' not in st.session_state:
            st.session_state.session_options = {
                'alpha_matting': True,
                'fg_threshold': 240,
                'bg_threshold': 10,
                'bg_color': '#1E1E1E', # Default to app background
                'use_sharpen': False,
                'use_contrast': False
            }

        # Simplified UI for options
        with st.expander("✨ Fine-Tune Settings", expanded=False):
            st.session_state.session_options['alpha_matting'] = st.toggle(
                "Enable Alpha Matting", 
                value=st.session_state.session_options['alpha_matting'],
                help="Improves edge quality, especially for hair and fur. May increase processing time."
            )
            st.session_state.session_options['fg_threshold'] = st.slider(
                "Foreground Threshold", 0, 255, 
                st.session_state.session_options['fg_threshold'],
                help="Higher values are more aggressive in classifying pixels as foreground."
            )
            st.session_state.session_options['bg_threshold'] = st.slider(
                "Background Threshold", 0, 255, 
                st.session_state.session_options['bg_threshold'],
                help="Lower values are more aggressive in classifying pixels as background."
            )
        
        with st.expander("🎨 Background & Effects", expanded=True):
             st.session_state.session_options['bg_color'] = st.color_picker(
                "Choose Background Color", 
                st.session_state.session_options['bg_color']
            )
             st.info("Set transparent by picking the color with 0 alpha (right slider).")

             st.session_state.session_options['use_sharpen'] = st.checkbox("Sharpen Before Processing")
             st.session_state.session_options['use_contrast'] = st.checkbox("Increase Contrast Before Processing")

    # --- Main Page Content ---
    st.title("🖼️ Advanced Image Background Remover")
    st.markdown(
        "Upload an image and use the sidebar controls to remove the background. "
        "Fine-tune the settings for the best results!"
    )
    
    col1, col2 = st.columns(2, gap="large")

    if my_upload is not None:
        if my_upload.size > MAX_FILE_SIZE:
            st.error(f"File size exceeds the limit of {MAX_FILE_SIZE/1024/1024:.0f}MB. Please upload a smaller image.")
        else:
            image_bytes = my_upload.getvalue()
            
            # Start timer and display progress
            start_time = time.time()
            
            original, fixed = process_image(image_bytes, st.session_state.session_options)
            
            if original and fixed:
                processing_time = time.time() - start_time
                st.sidebar.success(f"Processed in {processing_time:.2f} seconds")

                with col1:
                    display_image_card(original, "Original Image 📷", "orig")
                
                with col2:
                    display_image_card(fixed, "Processed Image ✨", "fixed")

                # Prepare for download
                file_format = "PNG" if st.session_state.session_options['bg_color'] == 'transparent' else "JPEG"
                mime_type = "image/png" if file_format == "PNG" else "image/jpeg"
                
                st.sidebar.markdown("---")
                st.sidebar.download_button(
                    label=f"Download Processed Image ({file_format})",
                    data=convert_image_to_bytes(fixed, format=file_format),
                    file_name=f"processed_{my_upload.name.split('.')[0]}.{file_format.lower()}",
                    mime=mime_type,
                    use_container_width=True
                )
    else:
        # Default view when no image is uploaded
        st.info("👋 Welcome! Upload an image using the sidebar to get started.")
        
        # Example image display
        default_image_path = "./zebra.jpg" # Make sure you have this image
        if os.path.exists(default_image_path):
            with open(default_image_path, "rb") as f:
                default_bytes = f.read()
            
            with col1:
                display_image_card(Image.open(BytesIO(default_bytes)), "Example: Original", "ex_orig")
            
            # Show a sample processed image
            sample_options = st.session_state.session_options.copy()
            _, sample_fixed = process_image(default_bytes, sample_options)
            if sample_fixed:
                 with col2:
                    display_image_card(sample_fixed, "Example: Processed", "ex_fixed")

# --- Run the App ---
if __name__ == "__main__":
    # Check for default image and inform user if missing

    
    main()
