#!/usr/bin/env python3
"""
stl_to_glb.py — Convert file STL sang GLB để chèn vào OhStem Project Builder.

CÀI ĐẶT (chỉ cần làm 1 lần):
    pip install trimesh pygltflib numpy --break-system-packages

CÁCH DÙNG:
    python stl_to_glb.py input.stl output.glb
    python stl_to_glb.py input.stl output.glb --color cc0000
    python stl_to_glb.py input.stl output.glb --no-center

LƯU Ý VỀ MÀU SẮC:
    File STL chuẩn KHÔNG lưu thông tin màu sắc (giới hạn của định dạng).
    Một số công cụ CAD/slicer xuất STL binary theo phần mở rộng
    "colored binary STL" (header bắt đầu bằng "COLOR="), script này sẽ
    tự động đọc và dùng màu đó nếu có. Nếu STL không có màu nhúng sẵn,
    bắt buộc phải truyền --color, nếu không script sẽ báo lỗi thay vì
    âm thầm xuất model màu xám mặc định.

    Nếu cần model nhiều màu / vật liệu thật, hãy dùng Blender:
    Import STL -> gán màu/material -> Export glTF 2.0 (.glb), tick "Include Materials".
"""

import argparse
import os
import struct
import sys

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import trimesh
except ImportError:
    print("Thiếu thư viện. Chạy lệnh sau rồi thử lại:")
    print("  pip install trimesh pygltflib numpy --break-system-packages")
    sys.exit(1)


def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Mã màu phải có 6 ký tự hex, ví dụ: cc0000")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return [r, g, b, 255]


def detect_embedded_stl_color(input_path):
    """
    Đọc header của binary STL để tìm màu nhúng sẵn theo phần mở rộng
    "colored binary STL" (VisCAM/SolidView/Magics): nếu 6 byte đầu
    header là "COLOR=", 4 byte tiếp theo là RGBA mặc định cho cả model.

    Trả về:
        (rgba hoặc None, has_per_face_override: bool)
    STL dạng ASCII hoặc binary không có phần mở rộng này -> (None, False).
    """
    with open(input_path, 'rb') as f:
        data = f.read()

    if len(data) < 84:
        return None, False

    header = data[:80]
    num_tris = struct.unpack('<I', data[80:84])[0]
    expected_size = 84 + 50 * num_tris
    if expected_size != len(data):
        # Không khớp kích thước binary STL chuẩn -> khả năng là ASCII STL
        return None, False

    global_rgba = None
    if header[:6] in (b'COLOR=', b'COLOR ', b'color='):
        r, g, b, a = header[6], header[7], header[8], header[9]
        global_rgba = [r, g, b, a]

    has_override = False
    offset = 84
    for _ in range(num_tris):
        attr = struct.unpack('<H', data[offset + 48:offset + 50])[0]
        if attr & 0x8000:
            has_override = True
            break
        offset += 50

    return global_rgba, has_override


def convert(input_path, output_path, color_hex=None, center=True):
    print(f"Đang đọc: {input_path}")

    detected_rgba, has_per_face_override = detect_embedded_stl_color(input_path)

    if color_hex is not None:
        rgba = hex_to_rgba(color_hex)
        print(f"  Dùng màu do người dùng chỉ định: #{color_hex}")
    elif detected_rgba is not None:
        rgba = detected_rgba
        print(f"  Phát hiện màu nhúng sẵn trong STL: rgba{tuple(rgba)}")
    else:
        raise ValueError(
            "STL này không có màu nhúng sẵn và bạn chưa truyền --color. "
            "Hãy chạy lại với --color <mã_hex>, ví dụ --color cc0000."
        )

    if has_per_face_override:
        print("  CẢNH BÁO: STL có màu khác nhau theo từng mặt (per-face), "
              "nhưng GLB xuất ra chỉ hỗ trợ 1 material đồng nhất -> toàn bộ "
              "model sẽ dùng 1 màu duy nhất ở trên. Muốn giữ nhiều màu thật, "
              "dùng Blender (xem HUONG_DAN.md).")

    mesh = trimesh.load(input_path)

    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces:    {len(mesh.faces)}")
    print(f"  Kích thước gốc: {mesh.extents}")

    if center:
        # Căn giữa theo X/Y, đặt đáy chạm gốc tọa độ Z=0
        mesh.apply_translation([
            -(mesh.bounds[0][0] + mesh.bounds[1][0]) / 2,
            -(mesh.bounds[0][1] + mesh.bounds[1][1]) / 2,
            -mesh.bounds[0][2]
        ])
        print("  Đã căn giữa X/Y và đặt đáy tại Z=0")

    # Dùng PBR material (baseColorFactor) thay vì vertex colors — nhiều
    # trình xem glTF (kể cả OhStem) không hiển thị vertex colors, chỉ
    # đọc màu từ material.
    material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba,
        metallicFactor=0.0,
        roughnessFactor=0.8,
    )
    mesh.visual = trimesh.visual.TextureVisuals(material=material)

    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"  Đã xóa file cũ: {output_path}")

    mesh.export(output_path)
    print(f"Đã xuất: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert STL sang GLB cho OhStem")
    parser.add_argument("input", help="Đường dẫn file .stl đầu vào")
    parser.add_argument("output", help="Đường dẫn file .glb đầu ra")
    parser.add_argument("--color", default=None,
                         help="Mã màu hex, không có dấu # (bắt buộc nếu STL "
                              "không có màu nhúng sẵn)")
    parser.add_argument("--no-center", action="store_true",
                         help="Không tự động căn giữa / đặt đáy tại Z=0")
    args = parser.parse_args()

    try:
        convert(args.input, args.output, args.color, center=not args.no_center)
    except ValueError as e:
        print(f"Lỗi: {e}")
        sys.exit(1)
