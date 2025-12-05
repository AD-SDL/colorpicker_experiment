from opentrons import protocol_api

metadata = {
    'protocolName': 'Rainbow Checkered Dye Mixing',
    'author': 'PRISM',
    'description': 'Create a rainbow checkered pattern using red, yellow, and blue dyes',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    destination_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    # Load reservoirs for dyes
    red_reservoir = protocol.load_labware('nest_12_reservoir_15ml', '5')
    yellow_reservoir = protocol.load_labware('nest_12_reservoir_15ml', '8')
    blue_reservoir = protocol.load_labware('nest_12_reservoir_15ml', '6')

    # Load pipette
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips])

    # Red Dye transfers (steps 1-23)
    red_transfers = [
        ('A1', 100), ('A3', 96), ('A5', 91), ('A7', 87), ('A9', 83), ('A11', 78),
        ('B2', 74), ('B4', 70), ('B6', 65), ('B8', 61), ('B10', 57), ('B12', 52),
        ('C1', 48), ('C3', 43), ('C5', 39), ('C7', 35), ('C9', 30), ('C11', 26),
        ('D2', 22), ('D4', 17), ('D6', 13), ('D8', 9), ('D10', 4)
    ]

    for well, volume in red_transfers:
        p300.pick_up_tip()
        p300.transfer(
            volume,
            red_reservoir['A1'],
            destination_plate[well],
            new_tip='never'
        )
        p300.drop_tip()

    # Yellow Dye transfers (steps 24-69)
    yellow_transfers = [
        ('A3', 4), ('A5', 9), ('A7', 13), ('A9', 17), ('A11', 22),
        ('B2', 26), ('B4', 30), ('B6', 35), ('B8', 39), ('B10', 43), ('B12', 48),
        ('C1', 52), ('C3', 57), ('C5', 61), ('C7', 65), ('C9', 70), ('C11', 74),
        ('D2', 78), ('D4', 83), ('D6', 87), ('D8', 91), ('D10', 96), ('D12', 100),
        ('E1', 96), ('E3', 92), ('E5', 88), ('E7', 83), ('E9', 79), ('E11', 75),
        ('F2', 71), ('F4', 67), ('F6', 62), ('F8', 58), ('F10', 54), ('F12', 50),
        ('G1', 46), ('G3', 42), ('G5', 38), ('G7', 33), ('G9', 29), ('G11', 25),
        ('H2', 21), ('H4', 17), ('H6', 12), ('H8', 8), ('H10', 4)
    ]

    for well, volume in yellow_transfers:
        p300.pick_up_tip()
        p300.transfer(
            volume,
            yellow_reservoir['A1'],
            destination_plate[well],
            new_tip='never'
        )
        p300.drop_tip()

    # Blue Dye transfers (steps 70-93)
    blue_transfers = [
        ('E1', 4), ('E3', 8), ('E5', 12), ('E7', 17), ('E9', 21), ('E11', 25),
        ('F2', 29), ('F4', 33), ('F6', 38), ('F8', 42), ('F10', 46), ('F12', 50),
        ('G1', 54), ('G3', 58), ('G5', 62), ('G7', 67), ('G9', 71), ('G11', 75),
        ('H2', 79), ('H4', 83), ('H6', 88), ('H8', 92), ('H10', 96), ('H12', 100)
    ]

    for well, volume in blue_transfers:
        p300.pick_up_tip()
        p300.transfer(
            volume,
            blue_reservoir['A1'],
            destination_plate[well],
            new_tip='never'
        )
        p300.drop_tip()

    protocol.comment('Rainbow checkered pattern complete!')
