import sys
import cli
import gui

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cli.cli_main()
    else:
        app = gui.DatabaseSettingsApp()
        app.run()
