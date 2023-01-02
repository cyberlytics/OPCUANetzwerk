import time

from sensors.movement_sensor import MovementSensor

def test_movement_sensor_measurement_start_stop():
    movement_sensor = MovementSensor(17)

    print('Start measurement, stop it and then start it again')
    result = movement_sensor.start_measurement()
    assert result == True
    movement_sensor.stop_measurement()

    result = movement_sensor.start_measurement()
    assert result == True

    movement_sensor.stop_measurement()

def test_movement_sensor_measurement_double_start():
    movement_sensor = MovementSensor(17)

    print('Start measurement two times. Should return false')
    result = movement_sensor.start_measurement()
    assert result == True
    result = movement_sensor.start_measurement()
    assert result == False

    movement_sensor.stop_measurement()

def test_single_movement():
    movement_sensor = MovementSensor(17)
    movement_sensor.start_measurement()

    print('Please do a single movement now')
    time.sleep(10)

    assert movement_sensor.Presence == True

    movement_sensor.stop_measurement()

def test_repeated_movement():
    movement_sensor = MovementSensor(17)
    movement_sensor.start_measurement()

    print('Please do a single movement now')
    time.sleep(10)

    print('Please do another movement now')
    time.sleep(50)

    assert movement_sensor.Presence == True

    movement_sensor.stop_measurement()

def test_movement_timeout():
    movement_sensor = MovementSensor(17)
    movement_sensor.start_measurement()

    print('Please do a single movement now and ensure, that sensor does not trigger after that.')
    time.sleep(10)
    assert movement_sensor.Presence == True

    time.sleep(60)
    assert movement_sensor.Presence == False




