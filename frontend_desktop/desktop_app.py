import sys
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QLabel, QFileDialog, QGroupBox, QDialog
)
from PyQt5.QtCore import Qt


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Chemical Equipment Visualizer")
    window.resize(700, 550)

    main_layout = QVBoxLayout()
    main_layout.setSpacing(15)

    # ---------- HEADER ----------
    header_box = QGroupBox()
    header_layout = QVBoxLayout()

    title = QLabel("Chemical Equipment Visualizer")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size:20px; font-weight:bold;")
    header_layout.addWidget(title)

    upload_btn = QPushButton("Upload CSV")
    header_layout.addWidget(upload_btn, alignment=Qt.AlignCenter)

    download_btn = QPushButton("Download PDF Report")
    download_btn.setDisabled(True)
    header_layout.addWidget(download_btn, alignment=Qt.AlignCenter)

    header_box.setLayout(header_layout)
    main_layout.addWidget(header_box)

    # ---------- SUMMARY ----------
    summary_box = QGroupBox("Summary")
    summary_layout = QVBoxLayout()

    summary_label = QLabel("Upload a CSV file to view summary")
    summary_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    summary_layout.addWidget(summary_label)

    summary_box.setLayout(summary_layout)
    main_layout.addWidget(summary_box)

    # ---------- CHART ----------
    chart_box = QGroupBox("Equipment Type Distribution")
    chart_layout = QVBoxLayout()

    chart_container = QWidget()
    chart_container_layout = QVBoxLayout()
    chart_container.setLayout(chart_container_layout)
    chart_layout.addWidget(chart_container)

    chart_box.setLayout(chart_layout)
    main_layout.addWidget(chart_box)

    # ---------- HELPERS ----------
    def show_loading_dialog(text):
        dialog = QDialog(window)
        dialog.setWindowTitle("Please wait")
        dialog.setModal(True)
        dialog.setFixedSize(250, 100)

        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.show()
        QApplication.processEvents()
        return dialog

    # ---------- LOGIC ----------
    def show_summary(data):
        summary = (
            f"Total Equipment: {data['total_count']}\n"
            f"Avg Flowrate: {data['average_flowrate']}\n"
            f"Avg Pressure: {data['average_pressure']}\n"
            f"Avg Temperature: {data['average_temperature']}"
        )
        summary_label.setText(summary)

    def show_chart(data):
        clear_layout(chart_container_layout)

        fig = Figure(figsize=(6, 3))
        canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot(111)

        types = data["equipment_type_distribution"]
        ax.bar(types.keys(), types.values())

        ax.set_xlabel("Type of Instrument")
        ax.set_ylabel("Count")

        chart_container_layout.addWidget(canvas)
        canvas.draw()

    def upload_csv():
        file_path, _ = QFileDialog.getOpenFileName(
            window, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        with open(file_path, "rb") as f:
            response = requests.post(
                "http://localhost:8000/api/upload/",
                files={"file": f}
            )

        if response.status_code == 200:
            data = response.json()
            upload_btn.setDisabled(True)
            upload_btn.setText("CSV Uploaded")
            download_btn.setEnabled(True)
            show_summary(data)
            show_chart(data)
        else:
            summary_label.setText("Upload failed")

    def download_pdf():
        upload_btn.setDisabled(True)
        download_btn.setDisabled(True)

        loading_dialog = show_loading_dialog("Downloading PDF...")

        try:
            response = requests.get(
                "http://localhost:8000/api/report/",
                auth=("my_name", "123456")
            )

            loading_dialog.close()

            if response.status_code != 200:
                summary_label.setText("Authentication failed")
                upload_btn.setDisabled(True)
                download_btn.setEnabled(True)
                return

            save_path, _ = QFileDialog.getSaveFileName(
                window,
                "Save PDF Report",
                "equipment_report.pdf",
                "PDF Files (*.pdf)"
            )

            if save_path:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                summary_label.setText("PDF downloaded successfully")

        except Exception:
            loading_dialog.close()
            summary_label.setText("Error downloading PDF")

        upload_btn.setDisabled(True)
        download_btn.setEnabled(True)

    upload_btn.clicked.connect(upload_csv)
    download_btn.clicked.connect(download_pdf)

    main_layout.addStretch()
    window.setLayout(main_layout)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
