import streamlit as st
import pandas as pd
from datetime import date
import openpyxl

def main():
    st.title("Excel to Tab-Delimited Text Converter")

    # File upload section
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.write('Processing')
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file,sheet_name='Receipt Import Template', skiprows=13)
            df['Ref #'].fillna(method ='ffill', inplace=True)
            df['Notes'].fillna(method ='ffill', inplace=True)
            df['Serial#'] = ''

            formatted_date = [x.strftime("%d%b%y") for x in df['Lot#']]

            # Convert date column to datetime format
            df['Lot#'] = formatted_date
            
            st.dataframe(df)
            
            
            today = date.today()
            # Convert to tab-delimited text
            output_text = df.to_csv(sep="\t", header=False, index=False)

            # Create a download link
            st.markdown(get_download_link(output_text), unsafe_allow_html=True)
        except Exception as e:
            st.write('An Error Occured.')
            st.error(f"Error reading the file: {e}")

def get_download_link(text):
    today = date.today()
    # Generate a download link for the text file
    href = f'<a href="data:text/plain;charset=utf-8,{text}" download="MayaReceiver{today}.txt">Download as Tab Delimited Text File</a>'
    return href

if __name__ == "__main__":
    main()
