requirements = {"robotType": "OT-2"}

from opentrons import protocol_api

metadata = {
    "protocolName": "Color Mixing Protocol",
    "author": "PRISM",
    "description": "Mix colors in a 96 well plate",
    "apiLevel": "2.12"
}

def run(protocol: protocol_api.ProtocolContext):
    deck = {}
    pipettes = {}

    ################
    # load labware #
    ################

    deck["2"] = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    deck["5"] = protocol.load_labware("nest_1_reservoir_195ml", "5")
    deck["5"].set_offset(x=0.00, y=0.00, z=1.50)
    deck["6"] = protocol.load_labware("nest_1_reservoir_195ml", "6")
    deck["6"].set_offset(x=0.00, y=0.00, z=1.50)
    deck["8"] = protocol.load_labware("nest_1_reservoir_195ml", "8")
    deck["8"].set_offset(x=0.00, y=0.00, z=1.50)
    deck["9"] = protocol.load_labware("nest_1_reservoir_195ml", "9")
    deck["9"].set_offset(x=0.00, y=0.00, z=1.50)
    deck["10"] = protocol.load_labware("opentrons_96_tiprack_300ul", "10")
    deck["11"] = protocol.load_labware("opentrons_96_tiprack_300ul", "11")
    pipettes["left"] = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[deck["10"], deck["11"]])

    ####################
    # execute commands #
    ####################

    # Red Dye transfers (steps 1-23)
    red_transfers = [
        ('A1', 100.0), ('A3', 96.0), ('A5', 91.0), ('A7', 87.0), ('A9', 83.0), ('A11', 78.0),
        ('B2', 74.0), ('B4', 70.0), ('B6', 65.0), ('B8', 61.0), ('B10', 57.0), ('B12', 52.0),
        ('C1', 48.0), ('C3', 43.0), ('C5', 39.0), ('C7', 35.0), ('C9', 30.0), ('C11', 26.0),
        ('D2', 22.0), ('D4', 17.0), ('D6', 13.0), ('D8', 9.0), ('D10', 4.0),
    ]

    # Yellow Dye transfers (steps 24-69)
    yellow_transfers = [
        ('A3', 4.0), ('A5', 9.0), ('A7', 13.0), ('A9', 17.0), ('A11', 22),
        ('B2', 26.0), ('B4', 30.0), ('B6', 35.0), ('B8', 39.0), ('B10', 43.0), ('B12', 48.0),
        ('C1', 52.0), ('C3', 57.0), ('C5', 61.0), ('C7', 65.0), ('C9', 70.0), ('C11', 74.0),
        ('D2', 78.0), ('D4', 83.0), ('D6', 87.0), ('D8', 91.0), ('D10', 96.0), ('D12', 100.0),
        ('E1', 96.0), ('E3', 92.0), ('E5', 88.0), ('E7', 83.0), ('E9', 79.0), ('E11', 75.0),
        ('F2', 71.0), ('F4', 67.0), ('F6', 62.0), ('F8', 58.0), ('F10', 54.0), ('F12', 50.0),
        ('G1', 46.0), ('G3', 42.0), ('G5', 38.0), ('G7', 33.0), ('G9', 29.0), ('G11', 25.0),
        ('H2', 21.0), ('H4', 17.0), ('H6', 12.0), ('H8', 8.0), ('H10', 4.0),
    ]

    # Blue Dye transfers (steps 70-93)
    blue_transfers = [
        ('E1', 4.0), ('E3', 8.0), ('E5', 12.0), ('E7', 17.0), ('E9', 21.0), ('E11', 25.0),
        ('F2', 29.0), ('F4', 33.0), ('F6', 38.0), ('F8', 42.0), ('F10', 46.0), ('F12', 50.0),
        ('G1', 54.0), ('G3', 58.0), ('G5', 62.0), ('G7', 67.0), ('G9', 71.0), ('G11', 75.0),
        ('H2', 79.0), ('H4', 83.0), ('H6', 88.0), ('H8', 92.0), ('H10', 96.0), ('H12', 100.0),
    ]

    pipettes["left"].pick_up_tip()
    for well, volume in red_transfers:
        pipettes["left"].well_bottom_clearance.aspirate = 1
        pipettes["left"].aspirate(volume, deck["5"]["A1"])
        pipettes["left"].well_bottom_clearance.dispense = 1
        pipettes["left"].dispense(volume, deck["2"][well])
        pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    for well, volume in blue_transfers:
        pipettes["left"].well_bottom_clearance.aspirate = 1
        pipettes["left"].aspirate(volume, deck["6"]["A1"])
        pipettes["left"].well_bottom_clearance.dispense = 1
        pipettes["left"].dispense(volume, deck["2"][well])
        pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    for well, volume in yellow_transfers:
        pipettes["left"].well_bottom_clearance.aspirate = 1
        pipettes["left"].aspirate(volume, deck["8"]["A1"])
        pipettes["left"].well_bottom_clearance.dispense = 1
        pipettes["left"].dispense(volume, deck["2"][well])
        pipettes["left"].blow_out()
    pipettes["left"].drop_tip()
