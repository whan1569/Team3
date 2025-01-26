import platform
import psutil
import cpuinfo

def get_system_info():
    # CPU 정보
    cpu_info = cpuinfo.get_cpu_info()
    cpu_name = cpu_info['brand_raw']
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    
    # 메모리 정보
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 ** 3)  # GB 단위로 변환
    available_memory = memory.available / (1024 ** 3)  # GB 단위로 변환
    
    # 시스템 플랫폼 정보
    system_platform = platform.system()
    system_version = platform.version()
    
    # 출력
    print(f"CPU: {cpu_name}")
    print(f"Physical Cores: {cpu_cores}")
    print(f"Logical Cores (Threads): {cpu_threads}")
    print(f"Total Memory: {total_memory:.2f} GB")
    print(f"Available Memory: {available_memory:.2f} GB")
    print(f"Platform: {system_platform}")
    print(f"Platform Version: {system_version}")

get_system_info()
