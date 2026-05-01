import pandas as pd
from fpdf import FPDF
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class ReportGenerator:
    """Handles file generation and email delivery."""
    
    @staticmethod
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='HealthLogs')
        return output.getvalue()

    @staticmethod
    def to_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "Health Data Report", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.ln(10)
        
        # Table Headers
        pdf.cell(30, 10, "Date", 1)
        pdf.cell(40, 10, "Name", 1)
        pdf.cell(30, 10, "Calories", 1)
        pdf.cell(30, 10, "Weight", 1)
        pdf.ln()

        # Data Rows
        for _, row in df.iterrows():
            pdf.cell(30, 10, str(row['log_date']), 1)
            pdf.cell(40, 10, str(row['name']), 1)
            pdf.cell(30, 10, str(row['calories']), 1)
            pdf.cell(30, 10, str(row['weight']), 1)
            pdf.ln()
            
        return pdf.output(dest='S').encode('latin-1')

    @staticmethod
    def send_email(recipient_email, file_data, file_name):
        sender_email = "jmamato03@gmail.com"  # Update this
        app_password = "Mynameis!M1c2a3l!!"    # Update this
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Health Dashboard Report - {file_name}"

        part = MIMEBase('application', "octet-stream")
        part.set_payload(file_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
            return True
        except Exception as e:
            return str(e)