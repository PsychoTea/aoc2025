import functools
import sys 

class Device:
    all: list = [ ]

    def __init__(self: Device, name: str) -> None:
        self.name = name 
        self.outputs = [ ]
        self.is_you = name == "you"
        self.is_out = name == "out"
        self.is_fft = name == "fft"
        self.is_dac = name == "dac"

    def __repr__(self: Device) -> str:
        return f"Device: name: {self.name}, outputs: {len(self.outputs)}"

    def add(self: Device, device: Device) -> None:
        self.outputs.append(device)

    @functools.cache
    def walk(self: Device, start_device: Device, visited_dac: bool = False, visited_fft: bool = False) -> int:
        if self.is_dac:
            visited_dac = True 

        if self.is_fft:
            visited_fft = True 

        if self.is_out:
            # For part 1 we are only concerned with the number of paths which go
            # from 'you' -> 'out'
            if start_device.is_you:
                return 1
            
            # For part 2 we need to know the number of paths which traverse 
            # 'svr' -> 'out' but also pass through 'dac' and 'fft'
            if visited_dac and visited_fft:
                return 1
            
            return 0

        return sum([x.walk(start_device, visited_dac, visited_fft) for x in self.outputs])

    @classmethod 
    def Create(cls: Device, name: str) -> Device:
        new_device = Device(name)

        cls.all.append(new_device)

    @classmethod 
    def Count(cls: Device) -> int:
        return len(cls.all)

    @classmethod
    def Find(cls: Device, name: str) -> Device | None:
        matches = [x for x in cls.all if x.name == name]

        if len(matches) == 0:
            return None 

        assert len(matches) == 1, f"Expected 1 match for device '{name}' but found {len(matches)}!"

        return matches[0]

def create_devices(input: list[str]) -> None:
    # First pass, parse the input devices
    for line in input:
        parts = line.split(':')

        Device.Create(parts[0])

    Device.Create('out')

    for line in input:
        parts = line.split(':')

        device_name = parts[0]

        main_device = Device.Find(device_name)

        outputs = parts[1].strip(' ').strip('\n').split(' ')

        for output in outputs:
            output_device = Device.Find(output)

            main_device.add(output_device)

    print(f"Created {Device.Count()} devices")

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} [input.txt]")
        return 
    
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    create_devices(lines)

    start_device = Device.Find('you')

    if start_device != None:
        answer = start_device.walk(start_device)

        print(f"Part 1 answer: {answer}")

    start_device = Device.Find('svr')
    
    if start_device != None:
        answer = start_device.walk(start_device)

        print(f"Part 2 answer: {answer}")

if __name__ == "__main__": 
    main()
