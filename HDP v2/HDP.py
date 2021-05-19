import win32serviceutil
import subprocess
import win32service
import win32event
import sys
import time
import servicemanager
import socket
import os
from threading import Thread
import pickle
import pdb
class hang_file(Thread):
    def __init__(self,filepath):
        Thread.__init__(self)
        self.file_path=filepath
    def run(self):
        dbg=pdb.set_trace()
        f=open(self.file_path,'r')
        time.sleep(20)
        f.close()
class protectmyhddsvcstarter(win32serviceutil.ServiceFramework):
    _svc_name_ = "HDP"
    _svc_display_name_ = "HDP"
    _svc_description_ = "protects multiple hard disks from being formated"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.drives=self.get_drives()
    def get_drives(self):
        data_file=open('hdp.dat','rb')
        drives=pickle.load(data_file)
        drives.remove('_')
        data_file.close()
        return drives

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
        dbg=pdb.set_trace()
        while self.isrunning:
            for drive in self.drives:
                dr=drive+':\\dummy.hdp'
                hf=hang_file(dr)
                hf.start()
            time.sleep(25)
  
            
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        win32serviceutil.HandleCommandLine(protectmyhddsvcstarter)
    else:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(protectmyhddsvcstarter)
        servicemanager.StartServiceCtrlDispatcher()
    
    
