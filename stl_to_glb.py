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
    Script này chỉ gán 1 màu đồng nhất (mặc định xám) cho toàn bộ model.
    Nếu cần model nhiều màu / vật liệu thật, hãy dùng Blender:
    Import STL -> gán màu/material -> Export glTF 2.0 (.glb), tick "Include Materials".
"""

import argparse
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


def convert(input_path, output_path, color_hex="c8c8c8", center=True):
    print(f"Đang đọc: {input_path}")
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

    rgba = hex_to_rgba(color_hex)
    mesh.visual = trimesh.visual.ColorVisuals(mesh, vertex_colors=rgba)
    print(f"  Đã gán màu đồng nhất: #{color_hex}")

    mesh.export(output_path)
    print(f"Đã xuất: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert STL sang GLB cho OhStem")
    parser.add_argument("input", help="Đường dẫn file .stl đầu vào")
    parser.add_argument("output", help="Đường dẫn file .glb đầu ra")
    parser.add_argument("--color", default="c8c8c8",
                         help="Mã màu hex, không có dấu # (mặc định: c8c8c8 - xám)")
    parser.add_argument("--no-center", action="store_true",
                         help="Không tự động căn giữa / đặt đáy tại Z=0")
    args = parser.parse_args()

    convert(args.input, args.output, args.color, center=not args.no_center)
