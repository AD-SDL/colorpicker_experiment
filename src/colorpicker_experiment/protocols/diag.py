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

    # Transfer 1: Blue dye to H1
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["H1"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 2: Blue dye to G2
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["G2"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 3: Blue dye to F3
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["F3"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 4: Blue dye to E4
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["E4"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 5: Blue dye to D5
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["D5"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 6: Blue dye to C6
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["C6"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 7: Blue dye to B7
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["B7"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()

    # Transfer 8: Blue dye to A8
    pipettes["left"].pick_up_tip()
    pipettes["left"].well_bottom_clearance.aspirate = 1
    pipettes["left"].aspirate(100.0, deck["6"]["A1"])
    pipettes["left"].well_bottom_clearance.dispense = 1
    pipettes["left"].dispense(100.0, deck["2"]["A8"])
    pipettes["left"].blow_out()
    pipettes["left"].drop_tip()
