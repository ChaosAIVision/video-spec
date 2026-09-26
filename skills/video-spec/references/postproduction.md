# Hậu kỳ clip Flow: quy trình dùng lại

Đọc khi đã có clip và người dùng yêu cầu sửa giọng, lời, hình, nhịp dựng hoặc xuất video. Đây là nhánh hậu kỳ của `video-spec`; yêu cầu cụ thể của người dùng và bản đã duyệt quyết định phạm vi sửa. [Ca Abbott COPD và Ensure](abbott-postproduction-case.md) lưu chi tiết lịch sử để tra cứu khi gặp lỗi tương tự, không phải thông số mặc định.

## 1. Chọn đúng nguồn và giữ đường quay lại

- Xác định **file người dùng đang xem** bằng đường dẫn, thời lượng, fps và khung hình mẫu. Mốc giây chỉ có nghĩa trên đúng phiên bản đó; bản đã cắt có thể đổi cả thời lượng lẫn fps.
- Ghi thứ tự cảnh, phiên bản nguồn, người nói, lời cần giữ/sửa, overlay và ngoại lệ. Tên clip có thể thiếu số hoặc có `4.1`; dùng thứ tự kể chuyện đã duyệt.
- Giữ nguồn và bản đã duyệt. Xuất bản mới hoặc sao lưu rồi mới thay cùng đường dẫn. Sau một lần cắt, đo lại timeline trước khi sửa theo mốc giây tiếp theo.
- Khi người dùng yêu cầu file audio riêng, giao từng WAV và giữ video chưa ghép. Khi chỉ một câu hoặc khoảng im lặng lỗi, sửa đúng đoạn đó; khi người dùng yêu cầu tạo lại toàn bộ, làm toàn bộ.

## 2. Đồng nhất giọng và sửa lời

**Bản đồ giọng.** Lập bảng `cảnh → lượt nói → nhân vật → profile`. Chuyên gia/lời dẫn, khách và nhân viên là các giọng riêng. Xác nhận profile đúng người bằng mẫu nghe và nội dung nguồn trước khi tạo. Khi lồng tiếng, loại track lời cũ ở lượt được thay để tránh hai giọng nói chồng; giữ âm thanh khác theo yêu cầu.

**Tạo tự nhiên.** Với OmniVoice, ưu tiên tốc độ/thời lượng tự nhiên của mô hình. Chỉ ràng thời lượng khi có lý do nghe nhìn rõ ràng; ép một câu vào số giây của video từng làm phát âm méo, giọng thiếu cảm xúc và mất chữ cuối. Với câu quá ngắn hoặc giọng không ổn định, có thể tạo thêm ngữ cảnh nói tự nhiên sau câu đích rồi cắt **sau khi câu đích kết thúc trọn âm tiết**. Kiểm tra khoảng đệm cuối trước khi ghép hình; người dùng có thể tự chỉnh tốc độ của file WAV được giao.

**Chữ khó đọc.** Viết thử cách phát âm tiếng Việt mà người dùng đã duyệt, ví dụ “te le seo” cho telesales. Số tiền cần được **nói** đầy đủ; đầu vào số `979` có thể thành “chín bảy chín”. Viết bằng chữ, và nếu vẫn bị đọc tắt, tạo riêng các cụm “chín trăm” và “bảy mươi chín nghìn”, kiểm tra từng cụm rồi nối ở khoảng ngắt tự nhiên. Tương tự với tên sản phẩm, COPD, HPG/HMB: giữ đúng từ của **cảnh đó**, không tự thay theo cảnh khác. Bỏ các từ đệm như “hả” khi người dùng yêu cầu; không tự thêm “ờ” để lấp khoảng trống.

**Kiểm tra.** ASR và mốc từ giúp tìm chỗ thiếu/lặp/cắt, nhưng ASR thường chuẩn hóa số thành chữ số; “979” trong transcript không chứng minh giọng đã nói đủ sáu âm tiết. Đối chiếu từng cụm và nghe file thật khi có khả năng nghe. Nếu môi trường không phát âm thanh cho agent, nói rõ rằng đã kiểm tra bằng ASR/dạng sóng, không nhận là đã nghe. Nghe/kiểm tra cả đầu, cuối và khoảng sau khi đặt audio vào video. Nếu âm ở cuối bị cắt, sửa đoạn tiếng hoặc nới khoảng đệm; không cắt frame nếu người dùng chỉ yêu cầu sửa lời.

## 3. Cắt, nối và nhạc

- Tìm câu lỗi trong bản hiện tại bằng lời thoại, ASR, dạng sóng và hình. Ranh giới cắt đặt theo âm thật, giữ phụ âm đầu/cuối; kiểm tra trước–tại–sau điểm nối. Không lấy mốc từ một bản dựng cũ áp cho bản mới.
- Chọn hiệu ứng chuyển theo bản đã duyệt. “Shadow” ở ca cũ nghĩa là fade qua đen, nhưng lặp ở mọi clip từng tạo nhịp khó chịu và khoảng đen dài. Kiểm tra `blackdetect`, `silencedetect` và các frame sát ranh giới; bỏ delay không chủ ý.
- Nhạc nhỏ hơn lời, có fade ngắn ở ranh giới phần. Giữ nhạc riêng từng phân đoạn nếu đã duyệt; kiểm tra tổng mức âm và bản xuất cuối. Nếu chỉ thay audio, copy bitstream hình khi phù hợp.
- Khi nối title card và phần video, kiểm tra frame 0 của thẻ có chữ/logo, viền trên không hở, phụ đề không xuất hiện trước người nói. Trim luồng AAC dài hơn hình trước khi concat nếu nó gây lệch ở các điểm nối.

## 4. Đồ họa và bố cục hình

- Giữ overlay đúng nội dung và thời điểm: nhãn người nói chỉ hiện khi người đó nói; tình huống có điểm đúng/sai theo lời; chuyên gia chọn vài ý chính. Dùng gạch đầu dòng hoặc mục rõ ràng. Tránh ticker chữ chạy và mũi tên chỉ để trang trí.
- Logo, faceswap, nền và caption phải dùng **đúng phiên bản đã duyệt**. Soi viền tóc, áo trắng và vùng da ở vài frame chuyển động, đủ độ phân giải; nếu tách nền làm nhòe/răng cưa, quay lại checkpoint tốt hơn.
- Với split screen có dải trắng **nằm sẵn trong footage**, đo bề rộng và vị trí dải ở vài cảnh. Có thể crop dải ở giữa rồi scale hai nửa về cùng chiều rộng; áp dụng đúng các đoạn tình huống, giữ phần chuyên gia và thẻ chuyển nguyên vẹn. Kiểm tra phụ đề/overlay bắc qua tâm và các điểm vào/ra. Ví dụ ca Ensure: nguồn hai tình huống cùng `1280×720`; dải trắng không phải do player hay do độ phân giải khác nhau. Việc bỏ dải trắng **không** tự sửa kích thước khuôn mặt thay đổi giữa các cảnh Flow; muốn đồng nhất khuôn mặt cần căn khung riêng từng shot trước overlay hoặc kiểm tra giới hạn crop ở bản tổng.

## 5. Giao bản đã kiểm tra

1. Dùng `ffprobe` đối chiếu thời lượng, fps, kích thước, số frame và luồng audio; giải mã toàn bộ file bằng FFmpeg. Với audio copy, có thể so hash âm giải mã để xác nhận không đổi.
2. Xem các frame ở đầu/cuối, mọi cảnh sửa và các điểm chuyển; nghe audio nơi vừa thay nếu có khả năng. Kiểm tra logo, chữ, mép hình, bar, độ nét, lời đầu/cuối và khoảng im lặng.
3. Báo rõ điều đã sửa, điều còn giới hạn, đường dẫn tuyệt đối của file mới và bản nguồn/sao lưu. Nếu nhờ chép ra Desktop, kiểm tra file đúng bản rồi chép ra; không ghi đè file khác cùng tên.
