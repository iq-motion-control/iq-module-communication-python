import iqmotion as iq

vertiq = iq.RdModule()

print(f"com_port: {vertiq._com._ser_handle._port}")
print(vertiq.get("system_control", "firmware_version"))
