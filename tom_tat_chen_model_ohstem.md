# Hướng dẫn chèn model 3D tùy chỉnh (STL) vào OhStem Project Builder

## Mục tiêu

Chèn model 3D tự thiết kế (dạng file `.stl`) vào phần "Mục mở rộng" / "Thành
phần thiết kế" của OhStem VR Project Builder (`app.ohstem.vn/#!/vr/project-builder`).

## Tóm tắt quy trình

```
File .stl  →  convert sang .glb  →  host công khai (GitHub)  →
khai báo trong file .xml theo đúng schema OhStem  →  dán URL vào OhStem
```

---

## 1. Vì sao cần các bước này

- OhStem Project Builder không cho tải trực tiếp file `.stl` lên
- Toàn bộ model 3D trong hệ thống dùng định dạng **`.glb`** (glTF Binary)
- Model được khai báo qua file `.xml` theo 1 schema riêng, và URL của file
  XML đó được dán vào ô "Tìm kiếm hoặc nhập URL của thư viện mở rộng"
- Schema này được xác nhận bằng cách bắt request thật qua DevTools (Network
  tab) của trình duyệt khi mở 1 pack có sẵn (`technic_bricks_ext.xml`)

## 2. Schema XML đã xác nhận

Ví dụ tối giản (chỉ 1 model):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<toolbox>
  <category id="ten_id_duy_nhat"
            name_en="Tên tiếng Anh"
            name_vi="Tên tiếng Việt"
            icon="🏗️"
            colour="#2196F3">
    <subcategory name_en="Group Name" name_vi="Tên nhóm" icon="📦">
      <part type="Box"
            name_en="Part Name EN"
            name_vi="Tên chi tiết"
            icon="data:image/png;base64,<ảnh preview nhỏ, có thể để tạm>"
            model_path="https://.../ten_model.glb">
      </part>
    </subcategory>
  </category>
</toolbox>
```

Ghi chú:
- `model_path` phải là **URL công khai (http/https)** trỏ trực tiếp tới
  file `.glb` — không dùng đường dẫn máy tính cá nhân
- File `.xml` này cũng phải được host ở URL công khai, vì OhStem sẽ
  `fetch()` nó từ trình duyệt
- `<snap_point>` bên trong `<part>` là tùy chọn, dùng để khai báo điểm khớp
  nối (không bắt buộc để hiển thị model cơ bản)

## 3. Convert STL sang GLB

### Cách A — Dùng script Python (tự động, nhanh)

```bash
pip install trimesh pygltflib numpy --break-system-packages
python stl_to_glb.py mo_hinh.stl mo_hinh.glb
python stl_to_glb.py mo_hinh.stl mo_hinh.glb --color 2196F3   # có màu tùy chỉnh
```

> **Giới hạn:** STL chuẩn không lưu thông tin màu sắc, nên script chỉ gán
> được 1 màu đồng nhất cho toàn bộ model.

### Cách B — Dùng Blender (giữ được màu/vật liệu thật)

1. File → Import → STL
2. Gán màu / vật liệu cho model trong Blender
3. File → Export → glTF 2.0 (`.glb`), nhớ tick **Include Materials**

## 4. Host file công khai (dùng GitHub)

1. Tạo 1 repository **Public** trên GitHub
2. Đẩy lên 2 file: model `.glb` và file khai báo `.xml`
3. Vào từng file trên GitHub → bấm nút **Raw** → copy URL, dạng:
   ```
   https://raw.githubusercontent.com/<tên-tài-khoản>/<tên-repo>/<nhánh>/<tên-file>
   ```
4. Dùng URL này điền vào `model_path` trong file `.xml`

> Có thể dùng dịch vụ khác thay GitHub nếu cần (Netlify Drop, v.v.), miễn
> là file truy cập được qua URL công khai và không bị chặn CORS.

## 5. Nạp vào OhStem

1. Mở Project Builder → vào **"Mục mở rộng"**
2. Dán URL của file `.xml` (đã host công khai) vào ô "Tìm kiếm hoặc nhập
   URL của thư viện mở rộng"
3. Card model sẽ hiện ra — bấm vào để xem chi tiết, kéo vào scene để chèn

## 6. Vấn đề đã biết

| Vấn đề | Nguyên nhân | Cách xử lý |
|---|---|---|
| Không đổi được màu model trong OhStem | STL không lưu màu; các part loại model thật không có thuộc tính `color` cấu hình được trong XML — màu được bake sẵn vào file `.glb` | Gán màu ngay lúc convert (Blender hoặc script với `--color`), không sửa được sau khi đã chèn vào OhStem |
| Báo lỗi "XML không hợp lệ" | Sai cấu trúc XML hoặc thiếu field bắt buộc | Đối chiếu lại với schema đã xác nhận ở mục 2 |

## 7. File tham khảo đã tạo trong quá trình này

- `stl_to_glb.py` — script tự convert STL sang GLB
- `stem_town_ext.xml` — file khai báo model mẫu, đúng schema
- `stem_town_model.glb` — model mẫu đã convert từ STL gốc

---

*Tài liệu này được tổng hợp từ quá trình thử nghiệm thực tế, dựa trên việc
phân tích request mạng (Network tab DevTools) của OhStem Project Builder —
không phải tài liệu chính thức từ OhStem.*
