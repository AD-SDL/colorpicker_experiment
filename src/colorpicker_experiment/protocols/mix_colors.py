requirements = {"robotType": "OT-2"}

from opentrons import protocol_api


metadata = {
    "protocolName": "Color Mixing Protocol",
    "author": "Abe astroka@anl.gov",
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


    deck["11"] = protocol.load_labware("opentrons_96_tiprack_1000ul", "11")

    pipettes[$pipette_side] = protocol.load_instrument("p1000_single_gen2", $pipette_side, tip_racks=[ deck["11"]])


    ####################
    # execute commands #
    ####################

    # Step one
    wells = $wells
    amounts = $amounts
    tubs = ["5", "6", "8", "9"]
    for index2, tub in enumerate(tubs):
        pipettes[$pipette_side].pick_up_tip()
        for index, well in enumerate(wells):

            pipettes[$pipette_side].aspirate(amounts[index][index2], deck[tub]["A1"])

            pipettes[$pipette_side].dispense(amounts[index][index2], deck["2"][well])

            pipettes[$pipette_side].blow_out()

        pipettes[$pipette_side].return_tip()
