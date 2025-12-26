import sys
from display.dhandler import Display
from winapi.ntfs import shell32

class Privileges:
    @staticmethod
    def is_admin():
        try:
            return shell32.IsUserAnAdmin()
        except Exception:
            return False

    @staticmethod
    def relaunch_as_admin(params):
        shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)

    @staticmethod
    def check_privileges(params):
        if not Privileges.is_admin():
            if Display.get_user_answer():
                Privileges.relaunch_as_admin(params)
            else:
                Display.show_end_program(1)               