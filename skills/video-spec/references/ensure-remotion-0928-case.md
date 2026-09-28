# Ca tham khảo: Ensure 0928 hậu kỳ Remotion và sửa một frame lỗi

Ca này ghi lại **cách làm**, không khóa nội dung hay timecode cho phim sau. Nguồn do người dùng lồng tiếng xong là `/Users/chaos/Desktop/project_3/0928_final.mov` (1920×1080, 30 fps, khoảng 153,1 giây). Người dùng yêu cầu hậu kỳ bằng Remotion theo mẫu title Abbott đã gửi: thẻ đề mục, logo, phụ đề, thẻ huấn luyện theo lời và nhạc nhẹ cho chuyên gia. Kế hoạch ở `plan-title-music-20260928.md` được người dùng chấp thuận bằng “oke, align”.

## Quy trình đã dùng

1. **Khóa nguồn và bản tham chiếu.** Giữ `0928_final.mov` nguyên vẹn. Dùng project Remotion riêng ở `postproduction_remotion_0928/`; giữ logo và nhạc đã có dưới `public/`. `src/timeline.ts` ghi bốn khoảng frame nguồn: mở đầu `[0,504)`, tình huống `[504,2808)`, phân tích `[2808,3504)`, thực hành `[3504,4588)`. Mỗi phần có thẻ 60 frame, nên video tổng thêm 240 frame. Cắt 5 frame chuyên gia lạc ở cuối nguồn sau câu hỏi thực hành.
2. **Dựng theo thời gian nguồn.** `src/cards.tsx` dựng thẻ nền navy, chữ/logo hiện từ frame 0. `src/film.tsx` đặt video nguồn, badge phần, 57 cue phụ đề, thẻ nhận xét `CẦN SỬA`/`LÀM ĐÚNG`, logo ở cảnh hội thoại và nhạc chỉ dưới thẻ/cảnh chuyên gia. Chữ cue được lấy từ ASR rồi sửa theo nội dung; ASR không thay việc nghe kiểm tra. Cảnh chuyên gia đã có logo ở góc trên; một patch alpha cục bộ che dấu lấp lánh Flow ở góc dưới.
3. **Render và căn tiếng.** Xuất preview Remotion 1920×1080, 30 fps. Bản render đầu có tiếng trễ khoảng 42,6 ms so với nguồn ở các đoạn không có nhạc; trim đầu audio theo độ trễ đo được và pad cuối tới thời lượng hình. Bản căn tiếng là `output/postproduction_0928/remotion_preview_aligned.mp4`, dài 160,933333 giây, 4.828 frame. Đây là giá trị của ca này, không phải hằng số Remotion.
4. **QA.** Xem bốn thẻ, các overlay và ranh giới phần; so khung hình với nguồn, đo độ trễ audio, đỉnh âm, `ffprobe`, giải mã toàn file. Khi người dùng báo “xe drop vào khung” ở giây 07, đối chiếu timeline: 2 giây thẻ mở đầu + 5 giây nguồn = 7 giây đầu ra. Nguồn có đúng **một frame lỗi** ở frame 150: xe/tài xế chồng lên chuyên gia. Nó đi qua Remotion thành frame 210, không phải do overlay Remotion sinh ra.
5. **Sửa hẹp và xác nhận.** Trích frame đầu ra 209, 210, 211. Sai khác ảnh trung bình ở ảnh thu nhỏ: `209↔210 ≈33`, `210↔211 ≈33`, trong khi `209↔211 ≈1,6`. Dùng frame 209 sạch thay riêng frame 210 trong một bản MP4 mới; mã hóa lại video, `-c:a copy`. Bản giao là `output/postproduction_0928/remotion_preview_aligned_v2.mp4`. Sau sửa, `209↔210 ≈0,95`, `210↔211 ≈1,76`; hash SHA-256 luồng AAC giống bản trước, 4.828 frame và 160,933333 giây giữ nguyên. Đã xem lại frame giây 07 và giải mã toàn file.

## Điều cần nhớ

- Đọc báo lỗi theo **timeline file người dùng đang xem** rồi quy đổi về nguồn trước khi quy trách nhiệm cho Remotion hay clip Flow. Một contact sheet theo frame quanh thời điểm lỗi tìm được frame đơn lẻ nhanh hơn xem mẫu mỗi nửa giây.
- Lỗi hình một frame và lời/nhạc đã đạt thì thay đúng frame hình, xuất tên mới, giữ audio bitstream. Đừng sửa `source.mp4` hoặc ghi đè bản đã giao nếu chỉ cần một bản vá hẹp.
- QA theo vài mốc ngẫu nhiên không bắt chắc một frame hỏng; kiểm tra frame trước/tại/sau **mỗi mốc người dùng nêu**. Nếu phát hiện frame hỏng ngay trong nguồn trước khi dựng, sửa ở tầng nguồn trung gian hoặc trong composition để các bản render sau không mang lại lỗi.
