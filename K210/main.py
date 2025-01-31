import sensor, image, time, lcd, ujson
import actuator, receiver, dataset, PinController
from machine import UART, I2C
import KPU as kpu

sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect
clock = time.clock()                # Create a clock object to track the FPS

# configure I2C to drive servo and ESC
i2c = I2C(I2C.I2C0, freq=100000, scl=0, sda=1)
controller = actuator.Actuator(i2c)

# configure the UART for transferring images
uart = UART(UART.UART2, 5000000, timeout=1000, read_buf_len=64)

# load model
model = kpu.load("/sd/model.kmodel")
kpu.set_outputs(model, 0, 1, 1, 1)

recorder = dataset.Dataset()
pin = PinController.Pin(controller)

# The receiver initialization is completed, which means that the K210 is
# fully initialized, so it is placed at the end
esp32_data = receiver.Receiver(controller, pin)
print("[I] K210 initialized")

def range_limit(value, range_min = -1, range_max = 1):
    if (value < range_min):
        value = range_min
    elif (value > range_max):
        value = range_max
    return value
#img_arr = bytearray([0xff,0xd8,0xff,0xe0,0x0,0x10,0x4a,0x46,0x49,0x46,0x0,0x1,0x1,0x0,0x0,0x1,0x0,0x1,0x0,0x0,0xff,0xdb,0x0,0x84,0x0,0x50,0x37,0x3c,0x46,0x3c,0x32,0x50,0x46,0x41,0x46,0x5a,0x55,0x50,0x5f,0x78,0xc8,0x82,0x78,0x6e,0x6e,0x78,0xf5,0xaf,0xb9,0x91,0xc8,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x1,0x55,0x5a,0x5a,0x78,0x69,0x78,0xeb,0x82,0x82,0xeb,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xc0,0x0,0x11,0x8,0x0,0xf0,0x1,0x40,0x3,0x1,0x22,0x0,0x2,0x11,0x1,0x3,0x11,0x1,0xff,0xc4,0x1,0xa2,0x0,0x0,0x1,0x5,0x1,0x1,0x1,0x1,0x1,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0xa,0xb,0x10,0x0,0x2,0x1,0x3,0x3,0x2,0x4,0x3,0x5,0x5,0x4,0x4,0x0,0x0,0x1,0x7d,0x1,0x2,0x3,0x0,0x4,0x11,0x5,0x12,0x21,0x31,0x41,0x6,0x13,0x51,0x61,0x7,0x22,0x71,0x14,0x32,0x81,0x91,0xa1,0x8,0x23,0x42,0xb1,0xc1,0x15,0x52,0xd1,0xf0,0x24,0x33,0x62,0x72,0x82,0x9,0xa,0x16,0x17,0x18,0x19,0x1a,0x25,0x26,0x27,0x28,0x29,0x2a,0x34,0x35,0x36,0x37,0x38,0x39,0x3a,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4a,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5a,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x73,0x74,0x75,0x76,0x77,0x78,0x79,0x7a,0x83,0x84,0x85,0x86,0x87,0x88,0x89,0x8a,0x92,0x93,0x94,0x95,0x96,0x97,0x98,0x99,0x9a,0xa2,0xa3,0xa4,0xa5,0xa6,0xa7,0xa8,0xa9,0xaa,0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9,0xba,0xc2,0xc3,0xc4,0xc5,0xc6,0xc7,0xc8,0xc9,0xca,0xd2,0xd3,0xd4,0xd5,0xd6,0xd7,0xd8,0xd9,0xda,0xe1,0xe2,0xe3,0xe4,0xe5,0xe6,0xe7,0xe8,0xe9,0xea,0xf1,0xf2,0xf3,0xf4,0xf5,0xf6,0xf7,0xf8,0xf9,0xfa,0x1,0x0,0x3,0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0xa,0xb,0x11,0x0,0x2,0x1,0x2,0x4,0x4,0x3,0x4,0x7,0x5,0x4,0x4,0x0,0x1,0x2,0x77,0x0,0x1,0x2,0x3,0x11,0x4,0x5,0x21,0x31,0x6,0x12,0x41,0x51,0x7,0x61,0x71,0x13,0x22,0x32,0x81,0x8,0x14,0x42,0x91,0xa1,0xb1,0xc1,0x9,0x23,0x33,0x52,0xf0,0x15,0x62,0x72,0xd1,0xa,0x16,0x24,0x34,0xe1,0x25,0xf1,0x17,0x18,0x19,0x1a,0x26,0x27,0x28,0x29,0x2a,0x35,0x36,0x37,0x38,0x39,0x3a,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4a,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5a,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x73,0x74,0x75,0x76,0x77,0x78,0x79,0x7a,0x82,0x83,0x84,0x85,0x86,0x87,0x88,0x89,0x8a,0x92,0x93,0x94,0x95,0x96,0x97,0x98,0x99,0x9a,0xa2,0xa3,0xa4,0xa5,0xa6,0xa7,0xa8,0xa9,0xaa,0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9,0xba,0xc2,0xc3,0xc4,0xc5,0xc6,0xc7,0xc8,0xc9,0xca,0xd2,0xd3,0xd4,0xd5,0xd6,0xd7,0xd8,0xd9,0xda,0xe2,0xe3,0xe4,0xe5,0xe6,0xe7,0xe8,0xe9,0xea,0xf2,0xf3,0xf4,0xf5,0xf6,0xf7,0xf8,0xf9,0xfa,0xff,0xda,0x0,0xc,0x3,0x1,0x0,0x2,0x11,0x3,0x11,0x0,0x3f,0x0,0x28,0xa2,0x8a,0x0,0x28,0xa2,0x8a,0x0,0x29,0x29,0x69,0x28,0x1,0x29,0x86,0x9d,0x4c,0x34,0x0,0xc3,0x49,0x4a,0x69,0x28,0x1,0x69,0xe2,0x9a,0x29,0xe2,0x80,0x1c,0x29,0xe2,0x90,0x52,0xd0,0x2,0xd2,0xd1,0x45,0x0,0x14,0x51,0x45,0x0,0x14,0x94,0xb4,0x50,0x2,0x51,0x4b,0x45,0x0,0x25,0x25,0x2d,0x14,0x0,0x94,0x51,0x45,0x0,0x14,0xd3,0x4e,0xa6,0x35,0x0,0x31,0x8d,0x45,0x4e,0x6a,0x6d,0x3,0x12,0x8a,0x5a,0x28,0x0,0xa9,0x5,0x34,0xa,0x90,0x50,0x21,0x68,0xa5,0xa2,0x90,0x9,0x45,0x14,0x50,0x4,0x72,0x52,0x47,0xd6,0x89,0x28,0x8e,0x98,0x16,0x68,0xa6,0xd2,0xd2,0x1,0x68,0xa2,0x8a,0x60,0x14,0x94,0xb4,0x94,0x0,0xd3,0x51,0x9a,0x79,0xa8,0xcd,0x0,0x36,0x96,0x92,0x9c,0x29,0x0,0xa2,0xa4,0x14,0xd1,0x52,0xa,0x60,0x28,0xa7,0x52,0xa,0x75,0x0,0x14,0x51,0x4b,0x40,0x9,0x45,0x2d,0x14,0x0,0x94,0x52,0xd1,0x40,0x9,0x49,0x4b,0x45,0x0,0x25,0x14,0xb4,0x50,0x3,0x68,0xa5,0xa6,0x9a,0x0,0x43,0x51,0x31,0xa7,0x31,0xa8,0x8d,0x21,0x8d,0xa2,0x8a,0x29,0x80,0x52,0x8a,0x4a,0x91,0x45,0x0,0x28,0x14,0xfa,0x0,0xa5,0xa4,0x20,0xa4,0xa5,0xa2,0x80,0x12,0x92,0x96,0x8a,0x0,0x86,0x4e,0xb4,0xb1,0xd3,0x5f,0xad,0x3e,0x353,0x80,0xa6,0x2,0x8a,0x78,0xa0,0xa,0x7e,0x29,0x0,0x52,0xd1,0x45,0x30,0xa,0x75,0x25,0x2d,0x0,0x2d,0x2d,0x25,0x2d,0x0,0x14,0xb4,0x51,0x40,0xb,0x4b,0x49,0x4b,0x40,0x5,0x2d,0x25,0x2d,0x0,0x14,0x51,0x45,0x0,0x2d,0x14,0x94,0x50,0x2,0xd2,0x51,0x49,0x40,0xb,0x49,0x45,0x14,0x0,0x51,0x49,0x45,0x0,0x14,0x94,0x51,0x40,0x5,0x30,0xd3,0xa9,0xa6,0x80,0x21,0x7a,0x86,0xa7,0x7a,0x81,0xa8,0x2,0x54,0xa9,0x45,0x40,0x95,0x30,0xa0,0x5,0x63,0x81,0x55,0x7e,0xf3,0xd4,0xb2,0xb5,0x24,0x23,0xbd,0x0,0x4b,0x45,0x14,0x50,0x2,0x51,0x45,0x14,0x80,0x84,0x53,0xc0,0xa0,0xa,0x78,0xa6,0x2,0xd2,0xd1,0x45,0x0,0x14,0xb4,0x51,0x40,0xb,0x4b,0x49,0x4b,0x40,0xb,0x4b,0x49,0x45,0x0,0x2d,0x2d,0x25,0x2d,0x0,0x2d,0x2d,0x25,0x14,0x0,0xb4,0xb4,0x94,0x50,0x2,0xd1,0x49,0x4b,0x40,0x5,0x14,0x51,0x40,0x5,0x14,0x52,0x50,0x1,0x45,0x14,0x50,0x2,0x51,0x45,0x14,0x0,0x94,0x51,0x49,0x40,0x5,0x21,0xa5,0xa4,0xa0,0x8,0x9a,0xab,0xb5,0x59,0x6a,0x81,0xe8,0x1,0xa9,0x53,0x67,0x8a,0xae,0x3a,0xd3,0xd9,0xa8,0x1,0xa7,0xe6,0x6a,0xb2,0xa3,0x2,0xa1,0x84,0x65,0xb3,0x53,0xd0,0x1,0x45,0x14,0x50,0x2,0x52,0x52,0xd1,0x40,0x8,0x5,0x3a,0x8a,0x28,0x0,0xa2,0x8a,0x28,0x1,0x68,0xa4,0xa5,0xa0,0x5,0xa5,0xa4,0xa2,0x80,0x16,0x96,0x92,0x96,0x80,0x16,0x96,0x9b,0x4b,0x40,0xb,0x4b,0x49,0x45,0x0,0x2d,0x2d,0x25,0x14,0x0,0xb4,0x52,0x51,0x40,0xb,0x45,0x25,0x14,0x0,0xb4,0x52,0x51,0x40,0x5,0x14,0x52,0x50,0x2,0xd2,0x51,0x49,0x40,0x5,0x14,0x52,0x50,0x1,0x45,0x14,0x94,0x0,0xd6,0xa8,0x1e,0xa7,0x35,0x13,0xd0,0x4,0x14,0x94,0xa6,0x85,0xeb,0x40,0x16,0x23,0x18,0x5a,0x7d,0x35,0x69,0xd4,0x0,0x51,0x45,0x14,0x0,0x94,0x51,0x45,0x0,0x2d,0x14,0x51,0x40,0x5,0x14,0x51,0x40,0x5,0x2d,0x25,0x2d,0x0,0x14,0xb4,0x94,0xb4,0x0,0xb4,0x52,0x52,0xd0,0x2,0xd1,0x49,0x4b,0x40,0xb,0x45,0x25,0x2d,0x0,0x2d,0x14,0x94,0x50,0x2,0xd1,0x49,0x4b,0x40,0x5,0x14,0x51,0x40,0x5,0x14,0x94,0x50,0x2,0xd2,0x51,0x45,0x0,0x14,0x94,0x51,0x40,0x5,0x14,0x94,0x50,0x1,0x45,0x25,0x14,0x0,0x86,0xa3,0x7a,0x92,0x98,0xd4,0x1,0x5d,0xa9,0x16,0x95,0xa9,0xb4,0x1,0x61,0x69,0xf5,0x12,0xd4,0x82,0x80,0x1d,0x49,0x45,0x14,0x0,0x51,0x45,0x14,0x0,0xb4,0x51,0x45,0x0,0x14,0x51,0x45,0x0,0x14,0x51,0x45,0x0,0x2d,0x14,0x94,0xb4,0x0,0xb4,0x51,0x45,0x0,0x2d,0x14,0x94,0xb4,0x0,0xb4,0x52,0x51,0x40,0xb,0x4b,0x49,0x45,0x0,0x2d,0x14,0x94,0x50,0x2,0xd1,0x49,0x45,0x0,0x2d,0x25,0x14,0x50,0x1,0x45,0x25,0x14,0x0,0xb4,0x94,0x52,0x50,0x2,0xd2,0x51,0x45,0x0,0x14,0x94,0x51,0x40,0x5,0x31,0xfa,0x53,0xaa,0x19,0x8d,0x0,0x44,0x69,0x29,0x45,0x6,0x80,0x1c,0xb5,0x30,0xaa,0xe2,0xa6,0x5a,0x0,0x92,0x8a,0x4a,0x5a,0x0,0x28,0xa4,0xa2,0x80,0x3f,0xff,0xd9])
while (True):
    pin.led_r()                     # blink, K210 is alive
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image
    #img.rotation_corr(z_rotation=90)# Image rotated 90°, fps halved
    #lcd.display(img)                # Display on LCD
    #print(clock.fps())              # Note: MaixPy's Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected

    if (pin.get_record() and esp32_data.get_recording() and controller.motor() > 0):
        recorder.save(img, controller.servo(), controller.motor())

    if (pin.get_auto_drive()):
        esp32_data.receive_lock(True)
        img = img.resize(160, 160)
        img.pix_to_ai()             # Sync "RGB888" memory block
        esp32_data.receive_lock(False)
        fmap = kpu.forward(model, img)
        plist = fmap[:]
        controller.servo(range_limit(plist[0]))         # angle
        # controller.motor(0.8)                           # speed
        print("[D] pridict angle: %f\t(%.2f fps)" % (plist[0], clock.fps()))

    # image transmission via UART
    if (False):
        img_compress = img.compressed(10)
        img_bytes = img_compress.to_bytes()
        img_len = img_compress.size()

        uart.write("\r\n--frame\r\n")
        uart.write("Access-Control-Allow-Origin: *\r\n")
        uart.write("Content-Length: " + str(img_len) + "\r\n")
        uart.write("Content-Type: image/jpeg\r\n\r\n")
        uart.write(img_bytes)

        print(img, img_len, clock.fps())
        #time.sleep_ms(2000)         # just for test
