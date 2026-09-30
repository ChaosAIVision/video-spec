# Hậu kỳ clip Flow: quy trình dùng lại

Đọc khi đã có clip và người dùng yêu cầu sửa giọng, lời, hình, nhịp dựng hoặc xuất video. Đây là nhánh hậu kỳ của `video-spec`; yêu cầu cụ thể của người dùng và bản đã duyệt quyết định phạm vi sửa. Các ca tham khảo: [Abbott COPD](abbott-postproduction-case.md) và [Ensure Remotion 0928](ensure-remotion-0928-case.md). Mốc giây và thông số của từng ca không phải mặc định cho dự án khác.

Khi phải ghép nhiều lượt WAV, sửa đoạn lồng tiếng hoặc xử lý một nhân vật bị đổi giọng giữa các câu, dùng [dialogue-audio-assembly](../../dialogue-audio-assembly/SKILL.md) cho bản đồ giọng, đặt tiếng trên timeline và QA audio. Nếu người dùng chỉ yêu cầu WAV, giao WAV sau khi kiểm tra; phần dựng video của tài liệu này chỉ áp dụng khi được yêu cầu.

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

## 6. Dựng đồ họa Remotion trên video đã lồng tiếng

Khi người dùng đã giao một phim có lời hoàn chỉnh và yêu cầu title, logo, phụ đề, thẻ giảng dạy và nhạc, dùng **chính phim đó** làm nguồn hình/tiếng. Xác nhận kế hoạch và bản tham chiếu đã được chấp thuận cho lượt dựng hiện tại; không lấy thoại hoặc timecode từ bản cũ.

1. `ffprobe` nguồn, ghi fps, thời lượng, số frame và ranh giới từng phần bằng **frame nguồn**. Lập ánh xạ `frame đầu ra = frame nguồn + tổng frame thẻ đã chèn trước đó`; dùng cùng ánh xạ cho phụ đề, thẻ ý chính và mọi báo lỗi theo giây đầu ra. Cắt frame thừa chỉ sau khi kiểm tra hình và âm ở cuối.
2. Dựng thẻ đề mục thành `Sequence` riêng. Chữ và logo phải đọc được ở frame 0; kiểm tra ảnh tĩnh của từng thẻ và frame đầu MP4. Dùng nguồn logo đúng bản đã duyệt. Nếu logo đã nằm trong footage chuyên gia, tránh đè logo thứ hai lên cùng vùng.
3. Đặt các overlay theo thời gian **nguồn** bên trong từng phần: nhãn người nói chỉ khi người đó nói, phụ đề từ lời thật của bản hiện tại, thẻ `CẦN SỬA`/`LÀM ĐÚNG` theo hành động. ASR là bản nháp để rà chữ và mốc, không phải bằng chứng đã nghe. Xem phần mở, các điểm chuyển, mọi thẻ, vùng mép và cảnh cuối ở bản render.
4. Nhạc dưới lời chuyên gia được giới hạn theo `Sequence`, fade ở ranh giới phần và đo mức sau khi trộn. Sau render, đo độ trễ tiếng so với nguồn ở vài đoạn **không có nhạc**; nếu có lệch, sửa theo độ trễ đo được rồi xác nhận lại. Không áp một giá trị bù cố định cho các bản render khác.
5. Nếu một hình lạ lóe lên trong một frame, đối chiếu cùng frame trên nguồn, file trung gian và bản xuất trước khi sửa. Trích frame trước/tại/sau; một frame giữa khác mạnh trong khi hai frame ngoài gần giống nhau là tín hiệu hữu ích. Khi chỉ đúng một frame hình bị hỏng, có thể thay bằng frame sạch liền kề trên **bản xuất mới**, giữ nguyên luồng audio bằng `-c:a copy`. Kiểm tra lại ba frame và hash luồng audio; thay một frame không đòi dựng lại toàn bộ thoại hoặc đồ họa.
6. `ffprobe` bản cuối, giải mã toàn file và so thời lượng, fps, số frame, hình tại điểm sửa, audio và các điểm nối. Giữ bản nguồn và bản preview trước; giao đường dẫn tuyệt đối của phiên bản mới.
