import pyrealsense2 as rs
import cv2
from pyzbar import pyzbar
import numpy as np

# RealSenseカメラの設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# カメラの起動
pipeline.start(config)

try:
    while True:
        # フレームの取得
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # フレームをOpenCV形式に変換
        frame = np.asanyarray(color_frame.get_data())

        # QRコードの読み取り
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        # QRコードが存在する場合は処理する
        if len(barcodes) > 0:
            for barcode in barcodes:
                # QRコードの位置を描画
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # QRコードのデータを取得して表示
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                cv2.putText(frame, f"{barcode_data} ({barcode_type})", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # フレームの表示
        cv2.imshow("QR Code Reader", frame)

        # 'q'キーが押されたら終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # プログラムの終了時にカメラを停止してウィンドウを閉じる
    pipeline.stop()
    cv2.destroyAllWindows()

