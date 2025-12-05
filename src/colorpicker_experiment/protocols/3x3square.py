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

    # Transfer 1: 50 µL yellow dye from reservoir A1 to destination plate A1
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["A1"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 2: 50 µL yellow dye from reservoir A1 to destination plate A2
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["A2"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 3: 50 µL yellow dye from reservoir A1 to destination plate A3
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["A3"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 4: 50 µL yellow dye from reservoir A1 to destination plate B1
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["B1"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 5: 50 µL yellow dye from reservoir A1 to destination plate B2
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["B2"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 6: 50 µL yellow dye from reservoir A1 to destination plate B3
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["B3"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 7: 50 µL yellow dye from reservoir A1 to destination plate C1
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["C1"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 8: 50 µL yellow dye from reservoir A1 to destination plate C2
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["C2"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 9: 50 µL yellow dye from reservoir A1 to destination plate C3
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["8"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["C3"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()
