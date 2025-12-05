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

    # Row A transfers (A1-A12)
    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A1"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A2"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A3"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A4"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A5"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A6"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A7"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A8"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A9"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A10"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A11"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["A12"])
    pipettes["left"].drop_tip()

    # Row C transfers (C1-C12)
    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C1"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C2"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C3"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C4"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C5"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C6"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C7"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C8"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C9"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C10"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C11"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["C12"])
    pipettes["left"].drop_tip()

    # Row E transfers (E1-E12)
    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E1"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E2"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E3"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E4"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E5"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E6"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E7"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E8"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E9"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E10"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E11"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["E12"])
    pipettes["left"].drop_tip()

    # Row G transfers (G1-G12)
    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G1"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G2"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G3"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G4"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G5"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G6"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G7"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G8"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G9"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G10"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G11"])
    pipettes["left"].drop_tip()

    pipettes["left"].pick_up_tip()
    pipettes["left"].aspirate(100.0, deck["5"]["A1"])
    pipettes["left"].dispense(100.0, deck["2"]["G12"])
    pipettes["left"].drop_tip()
