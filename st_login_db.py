import streamlit as st
from ggflight_sql import *
import datetime

# Print Hello morning or afternoon or evening with the current time
current_time = datetime.datetime.now().strftime("%H:%M")
if 5 <= int(current_time[:2]) < 12:
    st.markdown("""
                <hearder style='text-align: center;'>
                    <h1>Chào buổi sáng!</h1>
                    <p>Vui lòng đăng nhập vào cơ sở dữ liệu.</p>
                </hearder>
                """, unsafe_allow_html=True)
elif 12 <= int(current_time[:2]) < 18:
    st.markdown("""
                <hearder style='text-align: center;'>
                    <h1> Chào buổi chiều!</h1>
                    <p>Vui lòng đăng nhập vào cơ sở dữ liệu.</p>
                </hearder>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
                <hearder style='text-align: center;'>
                    <h1>Chào buổi tối!</h1>
                    <p>Vui lòng đăng nhập vào cơ sở dữ liệu.</p>
                </hearder>
                """, unsafe_allow_html=True)
    
# Create button to connect to Azure SQL
col1, col2, col3 = st.columns([1,1,1])
with col1:
    pass
with col3:
    pass
with col2:
    check_login_button = st.button("Đăng nhập Azure SQL")
def login_db(check_login_button):
    if check_login_button:
        conn = connect_db()
        if conn:
            st.success("Đăng nhập thành công!")
            return conn
        st.error("Gặp lỗi kết nối đến cơ sở dữ liệu. Vui lòng thử lại!")
    return None

if login_db(check_login_button) != None:
    # Go to `st_main.py` to see the next snippet
    import st_main
    