import win32gui
import win32con
import win32api
import pyautogui
import time


class PUBG_Coord_Verifier:
    def __init__(self):
        self.pubg_hwnd = None
        self.MAP_SIZE = 1050
        self.ref_width = 1000
        self.ref_height = 1000

        print("=" * 60)
        print("🎯 PUBG 绝对坐标标点验证工具 (硬编码版)")
        print("=" * 60)

    def find_pubg_window(self):
        def callback(hwnd, lst):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).upper()
                if "PUBG" in title or "BATTLEGROUNDS" in title:
                    if len(title) < 30:
                        lst.append(hwnd)

        windows = []
        win32gui.EnumWindows(callback, windows)

        if not windows:
            return False

        self.pubg_hwnd = windows[0]
        return True

    def get_game_window_info(self):
        if not self.pubg_hwnd: return None
        try:
            win_rect = win32gui.GetWindowRect(self.pubg_hwnd)
            client_rect = win32gui.GetClientRect(self.pubg_hwnd)

            client_w = client_rect[2]
            client_h = client_rect[3]

            border_x = (win_rect[2] - win_rect[0] - client_w) // 2
            border_y = (win_rect[3] - win_rect[1] - client_h) - border_x

            virtual_w, virtual_h = 1920, 1080

            return {
                'screen_pos': (win_rect[0], win_rect[1]),
                'border': (border_x, border_y),
                'real_client_size': (client_w, client_h),
                'virtual_offset': ((virtual_w - self.MAP_SIZE) // 2, (virtual_h - self.MAP_SIZE) // 2)
            }
        except Exception:
            return None

    def mark_point(self, input_x, input_y):
        if not self.find_pubg_window():
            print("❌ 未找到游戏窗口！请确保游戏正在运行。")
            return

        info = self.get_game_window_info()
        if not info:
            print("❌ 无法获取窗口信息！")
            return

        # 1. 将绝对坐标 (1000x1000) 转换为地图图片上的相对像素距离 (1050x1050)
        map_x = input_x * (self.MAP_SIZE / self.ref_width)
        map_y = input_y * (self.MAP_SIZE / self.ref_height)

        # 2. 映射到 1080p 的虚拟屏幕空间
        off_x, off_y = info['virtual_offset']
        virtual_x = off_x + map_x
        virtual_y = off_y + map_y

        # 3. 压缩回真实的低分辨率窗口坐标 (降维打击)
        real_w, real_h = info['real_client_size']
        real_x = int(virtual_x * (real_w / 1920.0))
        real_y = int(virtual_y * (real_h / 1080.0))

        # 4. 加上系统窗口位置和边框，算出真实的显示器物理坐标
        win_x, win_y = info['screen_pos']
        bor_x, bor_y = info['border']
        final_x = win_x + bor_x + real_x
        final_y = win_y + bor_y + real_y

        # 把游戏窗口切到最前
        print("⏳ 正在切回游戏窗口...")
        win32gui.SetForegroundWindow(self.pubg_hwnd)
        time.sleep(0.5)  # 稍微等半秒，让画面渲染完毕，防止切窗口太快导致没点上

        # 飞过去，右键标点！
        pyautogui.moveTo(final_x, final_y)
        time.sleep(0.1)
        pyautogui.rightClick()
        print(f"✅ 标点已下达！物理屏幕坐标: ({final_x}, {final_y})")

    def run(self, x, y):
        print(f"💡 准备验证坐标: X={x}, Y={y}")
        print("💡 请确保游戏内已按 M 打开大地图，并且缩放比例为默认大小！\n")
        self.mark_point(x, y)


if __name__ == "__main__":
    # ==========================================
    # 🎯 在这里修改你要验证的坐标！
    # ==========================================
    TEST_X = 339
    TEST_Y = 161
    # ==========================================

    verifier = PUBG_Coord_Verifier()
    verifier.run(TEST_X, TEST_Y)