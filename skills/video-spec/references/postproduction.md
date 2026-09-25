# Kinh nghiệm hậu kỳ video Google Flow nhiều clip

Đọc tài liệu này khi người dùng đã có clip Flow và yêu cầu đồng nhất giọng, sửa lời thoại, cắt đoạn, nối cảnh, thêm hình chuyển hoặc nhạc. Đây là nhánh hậu kỳ của `video-spec`, không thay thế quy trình duyệt kịch bản và hình tham chiếu trước khi tạo clip.

## Ca thực tế tạo nên tài liệu

Một video đào tạo tiếng Việt gồm cuộc gọi giữa bác Ba và nhân viên Anh, một đoạn chuyên gia nói trước nền trắng, rồi trở lại cuộc gọi. Các clip Flow có diễn xuất và ngữ điệu tương đối tốt nhưng hai nhân vật đổi chất giọng giữa các clip. Hậu kỳ phải thay một phần lời bằng giọng clone, giữ giọng lời dẫn riêng, sửa những âm tiết rè hoặc lơ lớ, nối các clip bằng hiệu ứng đã được người dùng chọn, chèn thẻ chuyển phần, cắt các câu dư và thêm nhạc nền.

Trong dự án này, bản merge trước khi người dùng tự cắt dài 249 giây ở 24 fps. Người dùng sau đó gửi một bản đã cắt bằng công cụ khác dài 208,533 giây ở 30 fps. Các mốc `2:46` trong bản đó **không còn trỏ vào cùng cảnh** như `2:46` của bản 249 giây; ngay cả lưới khung hình cũng đã đổi. Bản đã sửa xong phần lời, khoảng đen và trước khi thêm nhạc dài 199,267 giây. Các con số này là lịch sử của ca, không phải thông số mặc định cho dự án khác.

| Giai đoạn | Vấn đề đã gặp | Cách xử lý rút ra |
|---|---|---|
| Nhận clip Flow | Bác Ba và Anh đổi chất giọng giữa các clip | Dùng hai mẫu giọng được cung cấp, dựng profile OmniVoice riêng và gán từng lượt nói đúng người. |
| Sửa lời | Một số lượt nói của Anh lơ lớ hoặc rè; có clip nguồn mới | Sửa đúng lượt lỗi trên nguồn mới nhất, nghe lại cả câu và đoạn nối. |
| Dựng chuỗi | Có clip `4.1`, số clip không liên tục, lời dẫn cần giữ giọng riêng | Giữ thứ tự kể chuyện đã duyệt và bảng ngoại lệ, không áp dụng thay giọng hàng loạt. |
| Chuyển phần | Từ tình huống sang dinh dưỡng thiếu hình chuyển | Tạo thẻ chuyển tĩnh 3 giây và ghép theo quy tắc fade đã thống nhất. |
| Cắt tinh | Sau khi người dùng tự cắt, mốc thời gian thay đổi; lần cắt đầu bỏ quá tay | Sao lưu, xác định câu theo đúng bản hiện tại, chọn ranh giới theo tiếng và kiểm tra kết quả. |
| Hoàn thiện | Nhiều fade tạo đoạn đen dài; nhạc có thể át lời | Bỏ khoảng đen thừa, kiểm tra điểm nối, rồi mới trộn hai nền nhạc ở mức nhỏ. |

## 1. Chọn đúng bản nguồn và giữ đường quay lại

- Khi có nhiều file `merged`, bản đã cắt trên web, bản sửa lần 1 và bản có nhạc, xác nhận file nào là **bản người dùng đang xem**. Mốc thời gian của người dùng được hiểu theo bản đó.
- Trước khi thay đổi hình hoặc âm thanh, lưu một bản sao bất biến và kiểm tra bản sao giống nguồn. Mỗi lần xuất dùng tên mới; đừng ghi đè bản nguồn hoặc đổi đường dẫn cũ sang nội dung mới mà không nói rõ.
- Giữ một nhật ký ngắn: đường dẫn nguồn, thời lượng, fps, số kênh/tần số âm thanh, danh sách khoảng cắt trong *tọa độ của nguồn*, file đích và lý do. Khi đã cắt, tính lại timeline trước lần sửa tiếp theo.
- Clip có thể có tên lẻ như `4.1`, thứ tự kể chuyện khác thứ tự chữ cái, và số bị thiếu có chủ đích. Ghi thứ tự dựng đã được duyệt; không tự thêm clip thiếu hay sắp xếp lại theo tên file.

## 2. Đồng nhất giọng mà không làm mất diễn xuất

Lập bảng **clip → người nói → khoảng lời → hành động**. Trong ca này, bác Ba và Anh cần hai giọng cố định; các clip lời dẫn vẫn dùng giọng dẫn đã có. Một lệnh thay toàn bộ âm thanh sẽ xóa nhầm lời dẫn hoặc đổi sai nhân vật.

Khi bản gốc có ngữ điệu tốt, thử hướng chuyển giọng từ tiếng nói gốc sang giọng đích để giữ nhịp và cảm xúc. Khi phải tạo lại câu, dùng mẫu giọng sạch và tạo từng lượt nói. TTS clone có thể đúng màu giọng nhưng làm âm tiết tiếng Việt lơ lớ, đổi nhịp, hoặc rè ở cuối câu. Đừng ép thời lượng bằng kéo giãn mạnh nếu nó làm giọng méo. So sánh trực tiếp với lời gốc trong video, không chỉ nghe file giọng tách rời.

Ca này dùng OmniVoice trên máy xử lý riêng, với hai file mẫu giọng do người dùng đưa. Khi máy dựng và máy xử lý giọng khác nhau, ghi rõ phiên bản clip và profile giọng đang dùng, chuyển từng file có kiểm tra, rồi nghe bản đã ghép trên máy dựng. Không đưa mẫu giọng, profile clone hoặc file trung gian chứa dữ liệu giọng lên repo tài liệu.

Trước khi thay một đoạn, kiểm tra nội dung, đúng người nói, điểm bắt đầu/kết thúc, âm lượng, tiếng nền còn sót và độ khớp môi. Sau khi ghép lại, nghe cả khoảng trước và sau câu. Nếu chỉ một câu bị lỗi, sửa **câu đó** rồi kiểm tra lại; không dựng lại hàng loạt clip đang đạt.

## 3. Cắt câu dư theo lời nói thật, không chỉ theo số giây

Một mốc như `3:22` thường chỉ vị trí người dùng nghe lỗi, chưa phải ranh giới của câu cần bỏ. Tìm câu bằng transcript/ASR, rồi kiểm tra bằng dạng sóng, khoảng im lặng và khung hình. ASR giúp định vị nhưng có thể gán sai ranh giới từ, nhất là câu lặp. Giữ vài chục mili giây trước phụ âm đầu câu tiếp theo; cắt đúng mốc nguyên giây có thể làm mất chữ đầu.

Trong ca này, lần đầu cắt theo các khoảng nguyên giây đã bỏ quá nhiều. Người dùng hỏi lại bản backup. Cách sửa là trở lại đúng bản nguồn, xác nhận **cụm từ phải bỏ** và **cụm từ phải giữ**, rồi xuất bản mới. Với chuỗi sửa quanh `2:46`, yêu cầu tiến triển từ bỏ phần lặp “đi lại cũng không vững như trước”, đến bỏ cả câu “Đúng là dạo này chân tay tôi yếu đi”, câu đáp về cơ bắp, rồi câu YBG. Mỗi yêu cầu mới áp dụng trên bản mới nhất; không lấy lại mốc từ bản cũ.

Một điểm nối đạt yêu cầu khi nghe liên tục: câu trước kết thúc trọn nghĩa, câu sau giữ nguyên âm đầu, không còn lời dư, không có tiếng nổ hay mất đồng bộ môi. Có thể dùng fade âm thanh rất ngắn để tránh tiếng click, nhưng không làm chìm phụ âm đầu.

Nếu người dùng tự cắt bằng QuickTime Player: vùng giữa hai tay nắm vàng của **Trim** là phần **được giữ**. Muốn bỏ một đoạn ở giữa và giữ hai bên, chia clip ở hai đầu bằng `⌘T`, chọn mảnh giữa và xóa. Lưu bằng tên mới, rồi đo lại thời lượng và fps trước khi hậu kỳ tiếp.

## 4. Chuyển cảnh và khoảng đen

“Shadow” trong cuộc trao đổi này là cách nối clip bằng **fade về đen 0,5 giây ở cuối và fade từ đen 0,5 giây ở đầu**, áp dụng cả hình và âm. Không hiểu thành bóng đổ, phụ đề hoặc màn trập. Một thẻ tĩnh 3 giây “Tư vấn dinh dưỡng” được đặt giữa phần tình huống và phần tư vấn; thẻ cũng tuân theo cách fade đã chọn.

Fade tạo cảm giác mềm nhưng có thể chồng lên các khung đen đã có sẵn trong clip. Ca này phát sinh khoảng đen và im lặng hơn 1,5 giây quanh `2:47` sau nhiều lần cắt. Dùng `blackdetect` và `silencedetect` để xác định khoảng thực, xem khung ở trước/sau, rồi bỏ chính khoảng chờ. Nếu hình sáng trở lại muộn hơn tiếng nói một ít, có thể chọn khung hình sáng đầu tiên và giữ khung đó rất ngắn trong khi bảo toàn tiếng đầu câu. Kiểm tra lại trên **file đã xuất**, vì bộ lọc fade và bộ mã hóa có thể thay đổi cảm nhận ở điểm nối.

Không để một quy tắc “mọi chỗ đều phải fade” kéo dài màn đen. Một điểm nối ngắn, rõ lời và không có khoảng chết tốt hơn hiệu ứng được áp dụng máy móc.

## 5. Nhạc nền dưới lời thoại

Sao lưu bản video đã duyệt **trước khi ghép nhạc**. Xác định đoạn chuyên gia theo hình/lời trên timeline hiện tại; trong bản cuối của ca này khoảng `0:50–2:03`. Dùng nhạc nền nhẹ cho phần cuộc gọi, một giai điệu sáng hơn cho đoạn chuyên gia, và chuyển nhạc bằng fade ngắn. Các đoạn nói phải vẫn dễ nghe; nhạc nền là lớp hỗ trợ, không cạnh tranh với giọng.

Ca này dùng hai bản nhạc Mixkit: “My Little Prince” (Michael Ramir C.) và “Raising Me Higher” (Ahjay Stelino), theo [Mixkit Stock Music Free License](https://mixkit.co/license/modal/musicFree/). Kiểm tra lại giấy phép và kênh phát hành trước khi tái sử dụng nguồn nhạc cho dự án khác. Mức nhạc được chỉnh thấp hơn lời thoại khoảng 14–15 dB theo phép đo của ca; đây là điểm khởi đầu để nghe thử, không phải ngưỡng cố định. Dùng limiter để tránh đỉnh khi cộng nhiều nguồn âm. Nếu chỉ thay âm thanh, giữ nguyên bitstream hình khi có thể.

## 6. Kiểm tra trước khi giao

1. `ffprobe`: đúng thời lượng, fps, số khung hình, codec và thời lượng hai luồng hình/âm khớp nhau.
2. Giải mã trọn file bằng FFmpeg để phát hiện lỗi mã hóa.
3. Xem hình và nghe âm ở **mọi điểm vừa sửa**: trước, tại và sau điểm nối. Kiểm tra cụ thể câu phải còn, câu phải mất, giọng từng người, âm đầu/cuối, độ khớp môi, độ dài fade và nhạc không át lời.
4. Chạy phát hiện khung đen và im lặng quanh điểm nối. Một fade ngắn có chủ đích khác với khoảng đen kéo dài.
5. So sánh với bản sao lưu; báo đường dẫn rõ ràng của bản mới và bản trước. Khi người dùng hỏi “path video”, trả path tuyệt đối của file hoàn chỉnh, không chỉ tên file.

Transcript tự động, kiểm tra cấu trúc file và một khung hình xem trước chỉ là các phép kiểm phụ. Chúng không thay cho việc xem/nghe đoạn video đã xuất ở tốc độ bình thường.

## 7. Bài học từ bản dựng ba phần có đồ họa Remotion

Ở vòng dựng tiếp theo của cùng dự án, ba phần đã hậu kỳ riêng: **tình huống tư vấn**, **cùng chuyên gia phân tích**, **thực hành lại**. Người dùng duyệt từng phần trước, rồi yêu cầu thẻ mở đầu có logo Abbott, nhạc nhẹ cho chuyên gia và bản nối cuối. Đây là ví dụ về tiến trình duyệt của ca này, không phải khuôn cố định cho mọi video.

- **Đúng thứ tự, đúng bản đã duyệt.** Dùng các file hậu kỳ có voice OmniVoice, phụ đề và faceswap đã được chấp nhận; không quay về clip thô hoặc tự dựng lại lời thoại. Giữ ba phần tách riêng cho đến khi có yêu cầu nối. Khi nối, thứ tự là `thẻ 1 → tình huống → thẻ 2 → chuyên gia → thẻ 3 → thực hành`.
- **Chữ trên thẻ phải chỉ rõ nội dung.** Tiêu đề giữ nguyên tên ba phần; dòng phụ ngắn và cụ thể: cuộc gọi giữa Anh và bác Ba, dinh dưỡng cho người mắc COPD, rồi vận dụng vào cuộc tư vấn với bác Ba. Tránh những câu như “hiểu khó khăn và vai trò sản phẩm” khi người xem không biết cụ thể sẽ học gì. Tránh lặp lại tiêu đề ở nhãn nhỏ; dùng số phần hoặc nhãn có chức năng khác.
- **Bố cục điềm tĩnh.** Logo Abbott rõ nhưng không lấn tiêu đề. Chuyên gia chỉ cần vài ý chính; tình huống có thể có điểm nhấn theo từng nội dung nói, nhưng overlay xuất hiện đúng lúc câu bắt đầu. Không để phụ đề của bác Ba xuất hiện trên thẻ chuyển trước khi bác nói. Người dùng không muốn ticker chữ chạy và mũi tên trang trí vô nghĩa; nếu là các bước, dùng gạch đầu dòng hoặc các mục nhất quán. Các dấu tích cùng một hệ màu, không tô riêng một mục nếu không có ý nghĩa.
- **Kiểm tra khung đầu của MP4.** Hiệu ứng opacity từng làm tiêu đề biến mất ở frame 0: file vẫn có chữ sau 0,5 giây nhưng thumbnail xem trước trông như không có chữ. Nếu thẻ video được giao riêng, kiểm tra *frame 0 của chính MP4* và bảo đảm nội dung chính đọc được ngay. Kiểm tra cả mép trên: một dải màu 7 px trang trí đã làm người dùng thấy khung như hở viền.
- **Nền chuyên gia và tách nhân vật.** Khi ghép nhân vật áo trắng lên phông mới, viền tóc và áo có thể bị nhòe hoặc răng cưa. Không xem ảnh tổng thể thu nhỏ là đủ; phóng gần đường viền ở vài khung chuyển động. Nếu bản tách nền không đạt, quay lại bản chuyên gia đã duyệt hoặc để người dùng xử lý nền bằng công cụ họ chọn; giữ checkpoint trước lần ghép nền.
- **Nhạc dưới lời và qua thẻ phần.** Ở bản cuối, dùng lại bản nhạc tươi đã có trong dự án, âm lượng thấp dưới lời chuyên gia. Cho nhạc vào từ thẻ mở đầu phần chuyên gia, fade ngắn và kết thúc trước thẻ thực hành để chuyển phần có chủ ý. Kiểm tra tỉ lệ âm lượng bằng nghe thử và đo mức; một hệ số `volume=0.09` của ca chỉ là lựa chọn cho đúng nguồn nhạc đó.
- **Căn khớp khi nối.** Ở bản này, ba phần có hình lần lượt 50, 80, 80 giây, nhưng luồng âm AAC dài hơn hình khoảng 43–48 ms. Trim âm theo thời lượng hình trước khi concat để tránh dồn lệch điểm nối. Ba thẻ dài 3 giây, không có tiếng; tạo luồng âm im lặng cùng tần số/kênh. Bản cuối có 5.256 khung ở 24 fps, dài đúng 219 giây. Kiểm tra khung ngay trước/sau từng mốc nối và cả thời lượng hai luồng sau render.

Khi giao file, đưa đường dẫn tuyệt đối đến bản cuối; nếu người dùng nhờ chép ra Desktop, chép *đúng bản đã kiểm tra* và tránh ghi đè một bản khác cùng tên.
