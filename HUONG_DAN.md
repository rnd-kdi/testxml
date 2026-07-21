# Hướng dẫn sử dụng bộ file này

Folder này có 3 file:
- `stem_town_model.glb` — model 3D đã convert từ STL của bạn
- `stem_town_ext.xml` — file khai báo model theo đúng schema OhStem
- `catalog.xml` — file "bọc ngoài" dự phòng (chỉ dùng nếu cần)

**Việc duy nhất bạn cần làm:** đưa 3 file này lên một nơi có thể truy
cập bằng URL công khai (http/https), sau đó thay `{{BASE_URL}}`
trong 2 file XML bằng URL gốc thật.

---

## Cách 1 — GitHub (khuyên dùng, ổn định nhất)

1. Vào github.com, đăng nhập (hoặc tạo tài khoản miễn phí)
2. Tạo repository mới, chọn **Public**
3. Kéo thả cả 3 file trong folder này vào trang repo → Commit
4. Vào từng file `.glb` và `.xml` trên GitHub, bấm nút **Raw** → copy
   URL trên thanh địa chỉ, dạng:
   ```
   https://raw.githubusercontent.com/<tên-tài-khoản>/<tên-repo>/main/stem_town_model.glb
   ```
5. `{{BASE_URL}}` chính là phần trước tên file, tức:
   ```
   https://raw.githubusercontent.com/<tên-tài-khoản>/<tên-repo>/main
   ```
6. Mở `stem_town_ext.xml` và `catalog.xml` bằng Notepad (hoặc bất kỳ
   trình soạn thảo text nào), thay `{{BASE_URL}}` bằng URL ở bước 5,
   lưu lại, rồi upload đè lại lên GitHub.

---

## Cách 2 — Netlify Drop (không cần biết code, kéo-thả folder)

Phù hợp nếu không quen GitHub. Miễn phí, chỉ cần 1 tài khoản email.

1. Vào **app.netlify.com/drop**
2. Đăng nhập nhanh bằng email hoặc Google
3. **Kéo thả cả folder này** (không cần nén zip) vào ô trên trang
4. Netlify tự tạo 1 địa chỉ web dạng:
   ```
   https://ten-ngau-nhien-123.netlify.app
   ```
5. `{{BASE_URL}}` chính là địa chỉ đó (không có dấu `/` ở cuối)
6. Sửa 2 file XML như hướng dẫn ở Cách 1 (bước 6), rồi kéo-thả lại
   folder đã sửa lên Netlify Drop lần nữa để cập nhật

Netlify Drop cho phép truy cập file trực tiếp qua URL, hỗ trợ CORS
tốt (trình duyệt sẽ không chặn khi OhStem tải file từ đây).

---

## Cách 3 — Google Drive (dễ nhất nhưng có thể bị lỗi CORS)

1. Upload 3 file lên Google Drive
2. Chuột phải từng file → Chia sẻ → "Bất kỳ ai có đường liên kết"
3. Lấy ID file từ URL chia sẻ (đoạn ký tự dài giữa `/d/` và
   `/view`)
4. Dùng link tải trực tiếp dạng:
   ```
   https://drive.google.com/uc?export=download&id=<ID_FILE>
   ```

**Lưu ý:** Google Drive đôi khi chặn truy cập kiểu này từ trang web
khác (lỗi CORS) khiến OhStem không tải được. Nếu gặp lỗi, chuyển
sang Cách 1 hoặc Cách 2.

---

## Sau khi có {{BASE_URL}} và đã sửa file

1. Vào Project Builder trên OhStem → "Mục mở rộng"
2. Ở ô "Tìm kiếm hoặc nhập URL của thư viện mở rộng", dán URL đầy đủ
   tới `stem_town_ext.xml` (ví dụ:
   `https://raw.githubusercontent.com/ten/repo/main/stem_town_ext.xml`)
3. Nếu ô đó báo lỗi hoặc không nhận, thử lại bằng URL của
   `catalog.xml` thay thế
4. Nếu vẫn báo "XML không hợp lệ", chụp màn hình lỗi gửi lại để
   kiểm tra tiếp
