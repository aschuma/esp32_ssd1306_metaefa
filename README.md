```
                                                                                
                              _|_|_|      _|_|                  _|_|            
  _|_|      _|_|_|  _|_|_|          _|  _|    _|    _|_|      _|        _|_|_|  
_|_|_|_|  _|_|      _|    _|    _|_|        _|    _|_|_|_|  _|_|_|_|  _|    _|  
_|            _|_|  _|    _|        _|    _|      _|          _|      _|    _|  
  _|_|_|  _|_|_|    _|_|_|    _|_|_|    _|_|_|_|    _|_|_|    _|        _|_|_|  
                    _|                                                          
                    _|   
```

The aim of this project is to display the departure data of one ore more VVS stations on a esp32 microcontroller equipped with a oled ssd1306 display (Haltestellenmonitor). 
VVS is the Stuttgart public transport system. VVS provides the current timetable of relevant stations by a public available REST endpoint. 
Micropython is the programming language of choice.

Here is what you get when you deploy the application to your esp32 board:

![Demo](https://github.com/aschuma/esp32_ssd1306_metaefa/raw/master/esp32_ssd1306_metaefa.jpg)

The top line contains the current time.
The other lines hold the departure times, the tram/bus line number, the delay and a short name of the station (RH, SMi) of the tram or bus. 
The relevant tram/bus lines and station are configurable.


Links:
- http://www.vvs.de/
- https://github.com/opendata-stuttgart/metaEFA
- https://efa-api.asw.io/api/v1/
- https://www.espressif.com/en/products/hardware/esp32/overview
- https://www.aliexpress.com/wholesale?&SearchText=WEMS+ESP32+OLED+WiFi
- http://micropython.org/

# Onboarding 

This is just a brief description what steps have to be performed to enable the development of this application. Please consult google to get in depth details.

## Prepare development infrastructure

- Install the USB driver to enable board access: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
- Install python 3.x 
- Clone the repository
   ```
   git clone https://github.com/aschuma/esp32_ssd1306_metaefa.git
   ```
- Create a virtual environment, you may obtain more information about the steps below here: http://docs.python-guide.org/en/latest/dev/virtualenvs/ 
   ```
   cd esp32_ssd1306_metaefa/
   virtualenv py3 -p $(which python3)
   source py3/bin/activate
   ```
- Install development tools (`ampy`, `rshell`)   
   ```
   pip3 install -r requirements.txt 
   ```

## Micropython - prepare esp32 board

- Download the latest esp32 image from 
   https://micropython.org/download 
- Prepare the board
  ```
  esptool.py --port /dev/cu.SLAB_USBtoUART flash_id
  esptool.py --port /dev/cu.SLAB_USBtoUART erase_flash
  esptool.py --port /dev/cu.SLAB_USBtoUART write_flash -z 0x1000 <path-to-downlaoded-image>
  
  ```
  
## Micropython - check board access

- The subsequent command is for MacOS only. Similar tools are available for Linux and Windows. 
   ```
   screen /dev/cu.SLAB_USBtoUART 115200
   ```
   After that you will be connected to the micropython shell running on the board.
   You may leave the shell by typing `Ctrl-A`, `K` and `y.`
- File explorer
   ```
   rshell -p /dev/cu.SLAB_USBtoUART
   ```         
   The files on the board should be available at `/pyboard`
   You may copy files to the board by using the `cp` command.
   - https://github.com/dhylands/rshell
   
Please be aware that you can not use multiple shells simultaneously to the access the board.


## Deployment

- Copy `src/config.py.template` to `src/config.py` and adjust at least the wifi settings.
- Copy  recursively all files of `src` to the root directory of the board using the `rshell` tool or the `ampy` tool.
   - https://github.com/dhylands/rshell 
   - https://github.com/adafruit/ampy
   
# Finally

Be aware that my primary coding language is not python. So please forgive me my bad coding style. I'am still learning python and esp32 development.

Please feel free to issue a bug report or submit a PR. Any helping hand is welcome.
   
