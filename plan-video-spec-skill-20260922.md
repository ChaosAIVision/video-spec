# Plan: Đóng gói quy trình QC insight → Google Flow thành skill

## Objective
Tạo một Codex skill tái sử dụng mô tả đầy đủ quy trình biến dữ liệu lỗi QC và transcript thành kịch bản đào tạo nhiều scene, scene plan, rồi bộ prompt Google Flow có thể dùng ngay. Đóng gói skill trong repository `SWAT-AB/video-spec`, kiểm tra chất lượng, commit và push lên nhánh `main` để người dùng chấm quy trình.

## Approach
Skill sẽ dùng tên `video-spec` và tự động được gợi ý khi người dùng yêu cầu chuyển insight/transcript thành video đào tạo hoặc bộ prompt Flow. `SKILL.md` giữ luồng quyết định và các gate bắt buộc; hướng dẫn chi tiết, hợp đồng đầu ra và template được tách sang `references/` và `assets/` để giảm context load. Một script kiểm định sẽ kiểm tra bundle có đủ character sheet, master sheet, prompt từng scene, clip intake, tiếng Việt Unicode thật và các guardrail về video im lặng/không sinh chữ.

## Files
- **Create:** `README.md` — giới thiệu repository, cấu trúc và cách cài skill.
- **Create:** `skills/video-spec/SKILL.md` — entrypoint, trigger, workflow, gate và giới hạn quyền.
- **Create:** `skills/video-spec/agents/openai.yaml` — metadata hiển thị và prompt mặc định.
- **Create:** `skills/video-spec/references/workflow.md` — quy trình đầy đủ từ lọc lỗi đến nhận clip về.
- **Create:** `skills/video-spec/references/artifact-contracts.md` — tiêu chuẩn brief, script, scene plan và Flow handoff.
- **Create:** `skills/video-spec/references/prompt-engineering.md` — quy tắc continuity, nhân vật, camera, cảm xúc, tiếng Việt và negative constraints.
- **Create:** `skills/video-spec/assets/templates/` — template cho README handoff, character sheet, master prompt sheet, scene prompt và clip intake.
- **Create:** `skills/video-spec/scripts/validate_bundle.py` — kiểm định cấu trúc và các invariant của bundle.
- **Create:** `tests/test_validate_bundle.py` — kiểm tra validator với bundle hợp lệ và các lỗi quan trọng.
- **Create:** `.gitignore` — bỏ cache và file hệ thống.

## Risks & Trade-offs
- Repository công khai không nên chứa transcript, call ID, dữ liệu khách hàng hoặc bí mật nội bộ; ví dụ sẽ được tổng quát hóa.
- Skill sẽ phụ thuộc OpenMontage khi môi trường có sẵn, nhưng vẫn mô tả fallback artifact-first để không bị khóa vào một máy cụ thể.
- Push là thay đổi bên ngoài; người dùng đã chỉ định rõ remote và yêu cầu push. Nếu xác thực GitHub thất bại, dừng sau commit và báo lỗi chính xác.

## Implementation steps
1. Khởi tạo skill bằng `skill-creator` trong cấu trúc repository mới.
2. Viết `SKILL.md` với các gate: evidence → script → scene plan → Flow handoff → clip intake.
3. Viết ba reference, bảo toàn các bài học quan trọng từ quy trình đã thực hiện nhưng loại dữ liệu nhạy cảm.
4. Tạo các template paste-ready và script kiểm định bundle.
5. Thêm test, chạy `quick_validate.py`, unit test và một lần kiểm định fixture thực tế.
6. Review lại trigger, context pointers, Unicode tiếng Việt và ranh giới quyền/chi phí.
7. Khởi tạo Git repository, commit, đặt nhánh `main`, thêm remote `https://github.com/SWAT-AB/video-spec.git` và push.

## Open questions
None.
