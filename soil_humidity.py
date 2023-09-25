import spidev
import RPi.GPIO as GPIO
from time import sleep
Vref = 3.3
text = '{:.3f}'

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

spi = spidev.SpiDev() # インスタンス作成
spi.open(0,0) #port 0(SPI0 or SPI1),cs 0 (select channel 0~7)
spi.max_speed_hz = 1000000 # 1MHz (frequency)

denasu = 0
sleep(3)
try:
    for num in range(10):
        adc = spi.xfer2([0x06,0x00,0x00]) # データ送受信
        data = ((adc[1] & 0x0f) << 8) | adc[2] # 解析
        denasu += Vref*data/4096
        # print (str(Vref*data/4096) + "V" + " 閾値" + str(data)) # 測定電圧
        sleep(1)

except : # キー入力時、動作停止
    pass

print(text.format(denasu / 10))
spi.close()
GPIO.cleanup()
