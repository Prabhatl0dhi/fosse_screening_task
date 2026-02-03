from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes,permission_classes
from rest_framework.response import Response   
from rest_framework.parsers import MultiPartParser, FormParser 
from rest_framework.permissions import IsAuthenticated,AllowAny


from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import pandas as pd
import sqlite3
import json
 
 

@api_view(["POST"])
@permission_classes([AllowAny])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    # 1. Pandas analysis
    df = pd.read_csv(file)

    equipment_dist = {
        k: int(v) for k, v in df["Type"].value_counts().items()
    }

    summary = {
        "total_count": int(len(df)),
        "average_flowrate": round(float(df["Flowrate"].mean()),3),
        "average_pressure": round(float(df["Pressure"].mean()),3),
        "average_temperature": round(float(df["Temperature"].mean()),3),
        "equipment_type_distribution": equipment_dist
    }

    # 2. Store in SQLite
    conn = sqlite3.connect("instruments.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Instruments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_count INTEGER,
        average_flowrate REAL,
        average_pressure REAL,
        average_temperature REAL,
        equipment_type_distribution TEXT
    )
    """)

    cur.execute("""
    INSERT INTO Instruments (
        total_count,
        average_flowrate,
        average_pressure,
        average_temperature,
        equipment_type_distribution
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        summary["total_count"],
        summary["average_flowrate"],
        summary["average_pressure"],
        summary["average_temperature"],
        json.dumps(summary["equipment_type_distribution"])
    ))

    # 3. Keep only last 5 uploads
    cur.execute("""
    DELETE FROM Instruments
    WHERE id NOT IN (
        SELECT id FROM Instruments
        ORDER BY uploaded_at DESC
        LIMIT 5
    )
    """)

    conn.commit()
    conn.close()
    
    # 4. Return JSON to frontend
    print("FILES:", request.FILES)

    return Response(summary)



@api_view(["GET"])
@permission_classes([IsAuthenticated])

def generate_pdf(request):
    conn = sqlite3.connect("instruments.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT uploaded_at, total_count, average_flowrate,
               average_pressure, average_temperature,
               equipment_type_distribution
        FROM Instruments
        ORDER BY uploaded_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return HttpResponse("No data available", status=404)

    uploaded_at, total, flow, pressure, temp, dist = row
    dist = json.loads(dist)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=equipment_report.pdf"

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Chemical Equipment Report", styles["Title"]))
    elements.append(Paragraph(f"Uploaded at: {uploaded_at}", styles["Normal"]))
    elements.append(Paragraph(f"Total Equipment: {total}", styles["Normal"]))
    elements.append(Paragraph(f"Average Flowrate: {flow}", styles["Normal"]))
    elements.append(Paragraph(f"Average Pressure: {pressure}", styles["Normal"]))
    elements.append(Paragraph(f"Average Temperature: {temp}", styles["Normal"]))

    elements.append(Paragraph("Equipment Type Distribution:", styles["Heading2"]))
    for k, v in dist.items():
        elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(elements)
    return response

