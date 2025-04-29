import gradio as gr
from app.modules.status_dashboard import build_status_dashboard
from app.modules.timeline_dashboard import build_timeline_dashboard
from app.modules.admin_panel import build_admin_panel


def main():
    with gr.Blocks() as demo:
        # 레이아웃: 왼쪽에 사이드바, 오른쪽에 콘텐츠 영역
        with gr.Row():
            with gr.Column(scale=1):
                menu = gr.Radio(
                    choices=[
                        "모델 현황정보 대시보드",
                        "모델 타임라인 시각화",
                        "관리자 모델정보 등록",
                    ],
                    value="모델 현황정보 대시보드",
                    label="메뉴"
                )
            with gr.Column(scale=5):
                # 콘텐츠 영역에 각 대시보드 배치
                status_col = gr.Column(visible=True)
                with status_col:
                    build_status_dashboard()
                timeline_col = gr.Column(visible=False)
                with timeline_col:
                    build_timeline_dashboard()
                admin_col = gr.Column(visible=False)
                with admin_col:
                    build_admin_panel()
        # 메뉴 선택 시 보여줄 영역 전환 함수
        def switch_tab(choice):
            return (
                gr.update(visible=(choice == "모델 현황정보 대시보드")),
                gr.update(visible=(choice == "모델 타임라인 시각화")),
                gr.update(visible=(choice == "관리자 모델정보 등록")),
            )
        # 라디오 버튼 변경 이벤트 바인딩
        menu.change(
            fn=switch_tab,
            inputs=menu,
            outputs=[status_col, timeline_col, admin_col],
        )
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)


if __name__ == "__main__":
    main() 