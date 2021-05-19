import win32serviceutil
import subprocess
import win32service
import win32event
import sys
import time
import servicemanager
import socket
import os
class protectmyhddsvcstarter(win32serviceutil.ServiceFramework):
    _svc_name_ = "HDPsvcStarterF"
    _svc_display_name_ = "HDPsvcStarterF"
    _svc_description_ = """monitors the HardDiskProtect service.\n"
                           if in case you want to stop HDP service, make sure
                           to stop this service first. as this service will start it automatically."""

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
    def SvcDoRun(self):
        self.isrunning = True
        self.Run()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
    def SvcStop(self):
        self.isrunning = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        sys.exit()
        
    def Run(self):
        while self.isrunning:
            
            # check for HDP on disk G:\
            try:
                sock = socket.socket()
                sock.connect(("localhost", 27358))
                time.sleep(30)
                sock.close()
            except ConnectionRefusedError:
                os.chdir("G:\\")
                
                cmd = "harddiskprotect install"
                subprocess.run(cmd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                time.sleep(10)
                cmd = "harddiskprotect start"
                subprocess.run(cmd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                pass

            # check for HDP on disk H:\
            try:
                sock = socket.socket()
                sock.connect(('localhost', 27359))
                time.sleep(30)
                sock.close()
            except ConnectionRefusedError:
                os.chdir('E:\\')
                cmd = 'harddiskprotect install'
                subprocess.run(cmd , stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
                time.sleep(10)
                cmd = 'harddiskprotect start'
                subprocess.run(cmd , stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
                pass
            # check for HDP on disk F:\
            try:
                sock = socket.socket()
                sock.connect(('localhost',27360))
                time.slip(30)
                sock.close()
            except ConnectionRefusedError:
                os.chdir("F:\\")

                cmd = "harddiskprotect install"
                subprocess.run(cmd, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                time.sleep(10)
                cmd = "harddiskprotect start"
                subprocess.run(cmd, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                pass

            
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        win32serviceutil.HandleCommandLine(protectmyhddsvcstarter)
    else:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(protectmyhddsvcstarter)
        servicemanager.StartServiceCtrlDispatcher()
    
    
