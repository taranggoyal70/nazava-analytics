import os
import re

# Authentication code to add
AUTH_CODE = '''
# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_{page_key}"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")
'''

# Pages to update (excluding ones we already did)
pages_to_update = [
    "2_Traffic.py",
    "3_Sales.py",
    "4_Campaigns.py",
    "5_Customer_Service.py",
    "6_Products.py",
    "11_Automation_Bot.py",
    "12_Mass_Chat_Broadcasts.py",
    "13_Off_Platform_Traffic.py",
    "14_Shopee_PayLater.py",
    "15_Period_Comparison.py"
]

pages_dir = "/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/dashboard/pages"

for page_file in pages_to_update:
    page_path = os.path.join(pages_dir, page_file)
    page_key = page_file.replace(".py", "").replace("_", "").lower()
    
    with open(page_path, 'r') as f:
        content = f.read()
    
    # Check if already has auth
    if 'logged_in' in content and 'st.session_state' in content:
        print(f"✓ {page_file} already has authentication")
        continue
    
    # Find st.set_page_config and add auth after it
    pattern = r'(st\.set_page_config\([^)]+\))\s*\n'
    auth_with_key = AUTH_CODE.replace("{page_key}", page_key)
    replacement = r'\1\n' + auth_with_key + '\n'
    
    new_content = re.sub(pattern, replacement, content, count=1)
    
    if new_content != content:
        with open(page_path, 'w') as f:
            f.write(new_content)
        print(f"✅ Added authentication to {page_file}")
    else:
        print(f"⚠️  Could not update {page_file}")

print("\n🎉 Done! All pages now have authentication.")
