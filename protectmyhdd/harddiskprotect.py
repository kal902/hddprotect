import win32serviceutil
import win32service
import win32event
import sys
import servicemanager
import socket
class protectmyhdd(win32serviceutil.ServiceFramework):
    _svc_name_ = "HardDiskProtectF"
    _svc_display_name_ = "HardDiskProtectF"
    _svc_description_ = "protects the HardDisk from being formated\nby kaleab\nfor feedback use kaleab902@gmail.com"

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
            sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sv.bind(("localhost", 27360))
            sv.listen(1)
            sv.settimeout(30)
            while self.isrunning:
                try:
                    c,a=sv.accept()
                    break
                except socket.timeout:
                    pass
            sv.close()
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        win32serviceutil.HandleCommandLine(protectmyhdd)
    else:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(protectmyhdd)
        servicemanager.StartServiceCtrlDispatcher()
    
    
