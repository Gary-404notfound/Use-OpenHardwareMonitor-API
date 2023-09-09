import clr
import time

# 获取cpu温度
clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor import Hardware


class HardwareMonitor(object):
    def __init__(self):
        """
        obj用于实例化操作对象

        memo<x>Index————索引表：
        以__memoCPUIndex为例：
            type为list，属于传感器型（SensorType）索引，如CPUTemp对应每个核心的温度传感器
            type为int，属于硬件型（HardwareType）索引，如CPU对应硬件CPU

        """
        self.obj = Hardware.Computer()
        self.__memoCPUIndex = {'CPUTemp': [], 'CPUPower': [], 'CPULoad': [], 'CPU': int()}
        self.__memoGPUIndex = {'GPUTemp': [], 'GPUPower': [], 'GPULoad': [], 'GPU': int()}

    def __InitMonitor(self, CPU=1, GPU=1):
        """
        初始化Monitor
        :param CPU:CPU检测信息使能位，=1打开，=0关闭；默认开启
        :param GPU:GPU检测信息使能位，=1打开，=0关闭；默认开启
        :return:无
        """
        self.obj.CPUEnabled = CPU  # get the Info about CPU
        self.obj.GPUEnabled = GPU  # get the Info about GPU
        # self.obj.RAMEnabled = True
        # self.obj.MainboardEnabled = True
        # self.obj.HDDEnabled = True
        # self.obj.FanControllerEnabled = True
        self.obj.Open()

    def __BuildCPUMemo(self):
        """
        填充CPU索引表
        :return:无
        """
        for a in range(0, len(self.obj.Hardware)):
            if self.obj.Hardware[a].HardwareType == Hardware.HardwareType.CPU:
                self.__memoCPUIndex['CPU'] = a
                for b in range(0, len(self.obj.Hardware[a].Sensors)):
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Temperature:
                        self.__memoCPUIndex['CPUTemp'].append(b)
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Power:
                        self.__memoCPUIndex['CPUPower'].append(b)
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Load:
                        self.__memoCPUIndex['CPULoad'].append(b)

    def __BuildGPUMemo(self):
        """
        填充GPU索引表
        :return:无
        """
        for a in range(0, len(self.obj.Hardware)):
            if self.obj.Hardware[a].HardwareType == Hardware.HardwareType.GpuNvidia:  # 如果是AMD显卡则需把GpuNvidia改为GpuAti
                self.__memoGPUIndex['GPU'] = a
                for b in range(0, len(self.obj.Hardware[a].Sensors)):
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Temperature:
                        self.__memoGPUIndex['GPUTemp'].append(b)
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Power:
                        self.__memoGPUIndex['GPUPower'].append(b)
                    if self.obj.Hardware[a].Sensors[b].SensorType == Hardware.SensorType.Load:
                        self.__memoGPUIndex['GPULoad'].append(b)

    def Startup(self):
        """
        启动文件，初始化所有内容
        :return: 无
        """
        self.__InitMonitor()
        self.__BuildCPUMemo()
        self.__BuildGPUMemo()

    def GetMemo(self, HardwareType: int):
        """
        获取硬件索引表
        :param HardwareType:枚举类型，详见手册
        :return:__memo<x>Index （索引表）
        """
        if HardwareType == 2:
            return self.__memoCPUIndex
        elif HardwareType == 3:
            return self.__memoGPUIndex

    def GetCPUTempInfo(self):
        """
        获取CPU cores温度（每个core都有温度传感器）
        CPU Package温度
        :return:无
        """
        try:
            indexSum = len(self.__memoCPUIndex['CPUTemp'])
            HardwareIndex = self.__memoCPUIndex['CPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nCPU温度：")
                for i in range(0, indexSum-1):
                    print(f"CPU核心#{i+1}: "
                          f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUTemp'][i]].get_Value()} "
                          , flush=True)
                print(f"CPU Package#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUTemp'][indexSum-1]].get_Value()} "
                      , flush=True)
        except IndexError:
            print("\n初始化失败")

    def GetCPULoadInfo(self):
        """
        获取CPU负载，最后一个为总负载
        :return:无
        """
        try:
            indexSum = len(self.__memoCPUIndex['CPULoad'])
            HardwareIndex = self.__memoCPUIndex['CPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nCPU利用率：")
                for i in range(1, indexSum):
                    print(f"CPU核心#{i}: "
                          f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPULoad'][i]].get_Value()} "
                          "%", flush=True)
                print(f"CPU Total#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPULoad'][0]].get_Value()} "
                      "%\n", flush=True)
        except IndexError:
            print("\n初始化失败")

    def GetCPUPowerInfo(self):
        """
        获取CPU功耗
        :return: 无
        """
        try:
            indexSum = len(self.__memoCPUIndex['CPUPower'])
            HardwareIndex = self.__memoCPUIndex['CPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nCPU功耗：")
                print(f"CPU Package#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUPower'][0]].get_Value()} "
                      "W", flush=True)
                print(f"CPU Cores#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUPower'][1]].get_Value()} "
                      "W", flush=True)
                print(f"CPU Graphics#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUPower'][2]].get_Value()} "
                      "W", flush=True)
                print(f"CPU DRAM#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoCPUIndex['CPUPower'][3]].get_Value()} "
                      "W", flush=True)
        except IndexError:
            print("\n初始化失败")

    def GetGPUTempInfo(self):
        """
        获取GPU core的温度
        :return: 无
        """
        try:
            indexSum = len(self.__memoGPUIndex['GPUTemp'])
            HardwareIndex = self.__memoGPUIndex['GPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nGPU温度：")
                for i in range(0, indexSum):
                    print(f"GPU核心#{i+1}: "
                          f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPUTemp'][i]].get_Value()} "
                          , flush=True)
        except IndexError:
            print("\n初始化失败")  #

    def GetGPULoadInfo(self):
        """
        获取GPU负载以及各种占用
        :return: 无
        """
        try:
            indexSum = len(self.__memoGPUIndex['GPULoad'])
            HardwareIndex = self.__memoGPUIndex['GPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nGPU利用率：")
                print(f"GPU Core#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPULoad'][0]].get_Value()} "
                      "%\n", flush=True)
                print(f"GPU Frame Buffer#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPULoad'][1]].get_Value()} "
                      "%\n", flush=True)
                print(f"GPU Video Engine#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPULoad'][2]].get_Value()} "
                      "%\n", flush=True)
                print(f"GPU Bus Interface#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPULoad'][3]].get_Value()} "
                      "%\n", flush=True)
                print(f"GPU Memory#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPULoad'][4]].get_Value()} "
                      "%\n", flush=True)
        except IndexError:
            print("\n初始化失败")

    def GetGPUPowerInfo(self):
        """
        获取GPU功耗
        :return: 无
        """
        try:
            indexSum = len(self.__memoGPUIndex['GPUPower'])
            HardwareIndex = self.__memoGPUIndex['GPU']
            if indexSum == 0:
                raise IndexError
            else:
                print("\nGPU功耗：")
                print(f"GPU Power#: "
                      f"{self.obj.Hardware[HardwareIndex].Sensors[self.__memoGPUIndex['GPUPower'][0]].get_Value()} "
                      "W", flush=True)
        except IndexError:
            print("\n初始化失败")

    def HardwareUpdate(self):
        """
        更新传感器信息
        :return: 无
        """
        self.obj.Hardware[self.__memoCPUIndex['CPU']].Update()
        self.obj.Hardware[self.__memoGPUIndex['GPU']].Update()


def main():
    G = HardwareMonitor()
    G.Startup()
    # print(G.GetMemo(2))  # 打印CPU索引表
    # print(G.GetMemo(3))  # 打印GPU索引表
    while True:
        G.GetCPUTempInfo()
        G.GetGPUTempInfo()
        G.HardwareUpdate()
        time.sleep(2)  # 间隔2S刷新


if __name__ != '__main__':
    pass
else:
    main()
