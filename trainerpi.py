import bleCSC
import numpy
import threading


ROLLING_LENGTH = 2096.  # mm


power_curve = numpy.loadtxt("power-4.csv", delimiter=",")


def handle_speed_notification(wheel_speed: float, crank_speed: float) -> None:
    speed = wheel_speed * 3600. * ROLLING_LENGTH / 1e+6
    power = numpy.interp(speed, power_curve[:, 0], power_curve[:, 1])
    print("Wheel: {:2.0f} km/h, Power: {:3.0f} W, Crank: {:3.0f}".format(
        wheel_speed * 3600. * ROLLING_LENGTH / 1e+6,
        power,
        crank_speed * 60.
    ))


def wheel_thread_worker():
    wheel_sensor = bleCSC.CSCSensor("D0:AC:A5:BF:B7:52", handle_speed_notification)
    location_wheel = wheel_sensor.get_location()
    print("Location (wheel_sensor): {}".format(location_wheel))
    wheel_sensor.notifications(True)
    while True:
        try:
            if wheel_sensor.wait_for_notifications(1.0):
                continue
            print("Waiting for wheel...")
        except (KeyboardInterrupt, SystemExit):
            break


def crank_thread_worker():
    crank_sensor = bleCSC.CSCSensor("C6:F9:84:6A:C0:8E", handle_speed_notification)
    location_crank = crank_sensor.get_location()
    print("Location (crank_sensor): {}".format(location_crank))
    crank_sensor.notifications(True)
    while True:
        try:
            if crank_sensor.wait_for_notifications(1.0):
                continue
            print("Waiting for crank...")
        except (KeyboardInterrupt, SystemExit):
            break


wheel_thread = threading.Thread(target=wheel_thread_worker)
crank_thread = threading.Thread(target=crank_thread_worker)

wheel_thread.start()
crank_thread.start()

print("Exiting")
