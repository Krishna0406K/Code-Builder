"""
Ultra-simplified Streamlit app - Most reliable version
"""
import streamlit as st
import shutil
import zipfile
from pathlib import Path
from io import BytesIO

from agent.graph_2 import agent
from agent.tools import PROJECT_ROOT, init_project_root

# Page config
st.set_page_config(
    page_title="Code-Builder",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "generated" not in st.session_state:
    st.session_state.generated = False
if "project_path" not in st.session_state:
    st.session_state.project_path = None
if "error_message" not in st.session_state:
    st.session_state.error_message = None


def create_zip_file(source_dir: Path) -> BytesIO:
    """Create a zip file from the generated project directory."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(source_dir)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer


def get_file_tree(directory: Path, prefix=""):
    """Generate a visual file tree structure."""
    if not directory.exists():
        return ""
    
    tree = []
    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        tree.append(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir():
            extension = "    " if is_last else "│   "
            tree.append(get_file_tree(item, prefix + extension))
    
    return "\n".join(tree)


def read_file_content(file_path: Path) -> str:
    """Read and return file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def generate_project(user_prompt: str):
    """Generate project using the agent."""
    try:
        # Clear previous project
        if PROJECT_ROOT.exists():
            shutil.rmtree(PROJECT_ROOT)
        init_project_root()
        
        # Run agent
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": 100}
        )
        
        st.session_state.project_path = PROJECT_ROOT
        st.session_state.error_message = None
        return True
        
    except Exception as e:
        st.session_state.error_message = f"Generation failed: {str(e)}"
        return False


# Header
st.title("🤖 Code-Builder")

# Sidebar
with st.sidebar:
    st.header("📖 Tips")
    st.markdown("""
    **Keep it simple:**
    - Calculator
    - Todo list  
    - Landing page
    - Color picker
    
    **Mention tech:**
    - HTML, CSS, JavaScript
    - Python Flask
    - React
    """)
    
    st.markdown("---")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Your Prompt")
    user_prompt = st.text_area(
        "What do you want to build?",
        height=120,
        placeholder="Build a calculator in HTML, CSS, and JavaScript"
    )
    
    if st.button("🚀 Generate", type="primary", use_container_width=True):
        if user_prompt:
            st.session_state.generated = False
            st.session_state.error_message = None
            
            with st.spinner("🔨 Building your project..."):
                success = generate_project(user_prompt)
            
            if success:
                st.success("✅ Done!")
                st.session_state.generated = True
            else:
                st.error(f"❌ {st.session_state.error_message}")
        else:
            st.warning("⚠️ Please enter a prompt")

with col2:
    st.header("📦 Output")
    
    if st.session_state.generated and st.session_state.project_path:
        project_path = Path(st.session_state.project_path)
        
        if project_path.exists():
            # Download button
            zip_buffer = create_zip_file(project_path)
            st.download_button(
                label="⬇️ Download ZIP",
                data=zip_buffer,
                file_name="project.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            st.markdown("---")
            
            # File tree
            st.subheader("📁 Files")
            file_tree = get_file_tree(project_path)
            st.code(file_tree, language="")
        else:
            st.info("No files yet")
    else:
        st.info("👈 Enter a prompt to start")

# Preview section
if st.session_state.generated and st.session_state.project_path:
    st.markdown("---")
    st.header("👀 Preview")
    
    project_path = Path(st.session_state.project_path)
    
    if project_path.exists():
        all_files = [f for f in project_path.rglob('*') if f.is_file()]
        
        if all_files:
            file_names = [str(f.relative_to(project_path)) for f in all_files]
            selected_file = st.selectbox("Select file:", file_names)
            
            if selected_file:
                file_path = project_path / selected_file
                suffix = file_path.suffix.lower()
                
                language_map = {
                    '.py': 'python',
                    '.js': 'javascript',
                    '.html': 'html',
                    '.css': 'css',
                    '.json': 'json',
                }
                language = language_map.get(suffix, 'text')
                
                content = read_file_content(file_path)
                st.code(content, language=language)
                
                # HTML Preview
                if suffix == '.html':
                    st.markdown("---")
                    st.subheader("🌐 Live Preview")
                    with st.expander("View", expanded=True):
                        st.components.v1.html(content, height=500, scrolling=True)

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Krishna")
