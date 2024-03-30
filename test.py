import tkinter as tk

def answer():
    return "这是要显示的文本内容"

def create_transparent_window():
    # 创建主窗口
    window = tk.Tk()
    window.title("透明窗口")
    
    # 隐藏边框
    window.overrideredirect(True)
    
    # 获取系统窗口背景色
    system_bg_color = window.cget("bg")
    
    # 显示文本
    text = answer()
    label = tk.Label(window, text=text, bg=system_bg_color)
    label.pack(padx=20, pady=20)
    
    # 运行主循环
    window.mainloop()

if __name__ == "__main__":
    create_transparent_window()
