import streamlit as st
import pytesseract
from PIL import Image, ImageOps, ImageFilter
import platform
import os

import io

# Set page configuration
st.set_page_config(page_title="OCR App", page_icon="📝", layout="wide")

# OS Handling for Tesseract Path
if platform.system() == "Windows":
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    else:
        st.warning(f"Tesseract executable not found at {tesseract_path}. Please ensure Tesseract is installed.")

# Initialize session state for text
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

def process_image(image, grayscale, threshold, threshold_val):
    """Applies preprocessing to the image."""
    processed_image = image
    if grayscale:
        processed_image = ImageOps.grayscale(processed_image)
    if threshold:
        # Convert to grayscale first if not already
        if not grayscale:
             processed_image = ImageOps.grayscale(processed_image)
        # Apply threshold
        processed_image = processed_image.point(lambda p: 255 if p > threshold_val else 0)
    return processed_image

# Title and Description
st.title("📝 Optical Character Recognition (OCR) App")
st.markdown("Upload an image to extract text, edit it, and download as Text or PDF.")

# Sidebar - Image Preprocessing
st.sidebar.header("Image Preprocessing")
st.sidebar.markdown("Improve OCR accuracy for noisy images.")
use_grayscale = st.sidebar.checkbox("Convert to Grayscale", value=True)
use_threshold = st.sidebar.checkbox("Apply Thresholding", value=False)
threshold_value = st.sidebar.slider("Threshold Value", 0, 255, 128, disabled=not use_threshold)

# File Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load Image
    original_image = Image.open(uploaded_file)
    
    # Apply Preprocessing
    final_image = process_image(original_image, use_grayscale, use_threshold, threshold_value)

    # Layout: Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Image View")
        # Show processed image if preprocessing is on, otherwise original
        display_image = final_image if (use_grayscale or use_threshold) else original_image
        st.image(display_image, caption="Processed Image" if (use_grayscale or use_threshold) else "Original Image", use_container_width=True)
        
        # Extract Button
        if st.button("Extract Text & Generate PDF", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Get OCR Data (for confidence)
                    ocr_data = pytesseract.image_to_data(final_image, output_type=pytesseract.Output.DICT)
                    
                    # Calculate average confidence (ignoring empty results)
                    confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                    
                    # Extract Text
                    text_result = pytesseract.image_to_string(final_image)
                    
                    # Update Session State
                    st.session_state.extracted_text = text_result
                    st.session_state.avg_confidence = avg_confidence
                    
                    # Generate PDF bytes
                    st.session_state.pdf_bytes = pytesseract.image_to_pdf_or_hocr(final_image, extension='pdf')
                    
                    st.success("Extraction Complete!")
                    
                except pytesseract.TesseractNotFoundError:
                    st.error("Tesseract is not installed or not found.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with col2:
        st.subheader("Extracted Text")
        
        # Display Confidence if available
        if 'avg_confidence' in st.session_state:
            confidence_color = "green" if st.session_state.avg_confidence > 80 else "orange" if st.session_state.avg_confidence > 50 else "red"
            st.markdown(f"**Confidence Score:** :{confidence_color}[{st.session_state.avg_confidence:.2f}%]")

        # Text Area for Editing
        # We use a key to bind it to session state, but we also need to handle manual edits.
        # The text_area will update 'extracted_text' in session_state automatically if we use key='extracted_text'.
        # However, we updated it programmatically above. Streamlit handles this well.
        edited_text = st.text_area("Edit Text Here", value=st.session_state.extracted_text, height=500)
        
        # Update session state with edited text (in case user edits and then downloads)
        if edited_text != st.session_state.extracted_text:
             st.session_state.extracted_text = edited_text

        # Download Buttons
        if st.session_state.extracted_text:
            d_col1, d_col2 = st.columns(2)
            
            with d_col1:
                st.download_button(
                    label="Download Text (.txt)",
                    data=st.session_state.extracted_text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            
            with d_col2:
                if 'pdf_bytes' in st.session_state:
                    st.download_button(
                        label="Download PDF (.pdf)",
                        data=st.session_state.pdf_bytes,
                        file_name="extracted_document.pdf",
                        mime="application/pdf"
                    )
