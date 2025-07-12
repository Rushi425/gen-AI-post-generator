import streamlit as st
import post_generator
from few_shots import FewShotPosts

# Constants
LENGTH_OPTIONS = ['Short', 'Medium', 'Long']
LANGUAGE_OPTIONS = ['English', 'HinEnglish']


def main():
    # --- Streamlit Configuration ---
    st.set_page_config(
        page_title="LinkedIn Post Generator",
        page_icon="📝",
        layout="wide"
    )

    # --- Custom CSS and JS Injection for Styling and Copying ---
    st.markdown("""
    <style>
    /* Styling for the post preview box (ensures theme compatibility) */
    .post-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid;
        margin-top: 1em;
        white-space: pre-wrap; /* Ensures line breaks are preserved */
        word-wrap: break-word; 
        font-family: Arial, sans-serif;
    }

    /* Light Theme Styling for post-box */
    .stApp {
        /* Default colors for the box in light mode */
        --post-box-bg: #e7f0fc;
        --post-box-border: #c2c2c2;
        --post-box-text: #1a1a1a;
    }
    .post-box {
        background-color: var(--post-box-bg);
        border-color: var(--post-box-border);
        color: var(--post-box-text);
    }

    /* Dark Theme Styling adjustments for post-box */
    /* Streamlit's default dark mode applies a class to the root element. */
    .stApp.dark .post-box {
        --post-box-bg: #2b2b40;
        --post-box-border: #444;
        --post-box-text: #e0e0e0;
        background-color: var(--post-box-bg);
        border-color: var(--post-box-border);
        color: var(--post-box-text);
    }

    /* Style the Copy button */
    #copy-button {
        background-color: #0e76a8; /* LinkedIn blue */
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
        font-size: 16px;
        transition: background-color 0.2s;
    }
    #copy-button:hover {
        background-color: #005a87;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Title & Description ---
    st.title("📝 LinkedIn Post Generator")
    st.subheader("Generate engaging LinkedIn posts powered by Generative AI.")
    st.markdown(
        """
        Use the sidebar to configure your post preferences. 
        Click **Generate Post** to create your content. The generated post can be edited below.
        """
    )

    # --- Sidebar Configuration ---
    st.sidebar.header("Configuration")

    # Initialize FewShotPosts (assumes few_shots.py exists and FewShotPosts class is defined)
    fs = FewShotPosts()

    # Input selectors
    selected_tag = st.sidebar.selectbox("Post Topic", options=fs.get_tags())
    selected_length = st.sidebar.selectbox("Post Length", options=LENGTH_OPTIONS)
    selected_language = st.sidebar.selectbox("Language", options=LANGUAGE_OPTIONS)

    st.sidebar.markdown("---")
    generate_button = st.sidebar.button("🚀 Generate Post")

    # --- Post Generation and Display ---
    if generate_button:
        with st.spinner("Generating your LinkedIn post..."):
            # Call the generation function (assumes post_generator.py exists)
            try:
                post = post_generator.generate_post(selected_length, selected_language, selected_tag)
            except Exception as e:
                st.error(f"Error generating post: {e}")
                post = "Post generation failed. Please check the backend configuration."

        st.success(f"✅ Generated Post for **{selected_tag}** ({selected_length}, {selected_language}):")

        # Editable text area for review and refinement
        # The user can edit the content directly in this box.
        edited_post = st.text_area(
            "Review and modify the generated content:",
            value=post,
            height=250
        )

        # Styled Preview Box (Theme-compatible)
        st.markdown("### Post Preview")
        st.markdown(
            f"""
            <div class="post-box">
            {edited_post.replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Copy to Clipboard Button ---
        # We inject a button and JS to copy the content from the st.text_area.
        st.markdown(
            """
            <button id="copy-button">📋 Copy to Clipboard</button>
            <script>
            // JavaScript to handle the copy action
            const copyBtn = document.getElementById('copy-button');
            if (copyBtn) {
                copyBtn.onclick = () => {
                    // Find the Streamlit text area element (the editable box)
                    const textArea = document.querySelector('textarea'); 
                    if (textArea) {
                        // Use the Clipboard API to copy the text
                        navigator.clipboard.writeText(textArea.value);
                        copyBtn.innerText = '✅ Copied!';
                        // Reset the button text after 2 seconds
                        setTimeout(() => copyBtn.innerText = '📋 Copy to Clipboard', 2000);
                    }
                }
            }
            </script>
            """,
            unsafe_allow_html=True
        )

    else:
        # Initial prompt when the app loads
        st.info("⬅️ Please configure your preferences and click **Generate Post**.")

    # --- Footer ---
    st.markdown(
        """
        <hr style="margin-top: 2em;">
        <center>
        <small>Powered by Generative AI</small>
        </center>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()