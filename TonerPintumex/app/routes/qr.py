# import cv2


# def main() -> None:
#     detector = cv2.QRCodeDetector()

#     # 1) Abrir cámara. En Windows, CAP_DSHOW suele evitar errores/latencia.
#     camera_index = 0
#     cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#     if not cap.isOpened():
#         raise SystemExit("Error: No se pudo abrir la cámara.")

#     last_text = None

#     try:
#         while True:
#             # 2) Leer fotograma
#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: No se pudo recibir el fotograma (fin de la transmisión?).")
#                 break

#             # 3) Detectar y decodificar QR
#             text, points, _ = detector.detectAndDecode(frame)

#             if points is not None:
#                 pts = points.astype(int).reshape(-1, 2)
#                 cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

#             if text:
#                 if text != last_text:
#                     last_text = text
#                     print("QR leído:\n" + text)

#                 cv2.putText(
#                     frame,
#                     "QR detectado",
#                     (20, 40),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.0,
#                     (0, 255, 0),
#                     2,
#                     cv2.LINE_AA,
#                 )

#             # 4) Mostrar cámara
#             cv2.imshow("Mi Camara (q=salir)", frame)

#             # 5) Salir con q
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()